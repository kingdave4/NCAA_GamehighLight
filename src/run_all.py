# run_all.py

import subprocess
import time
from config import (
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BETWEEN_SCRIPTS
)

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    """Run a script with retry logic and a delay between retries."""
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully.")
            return  # Exit function if script runs successfully

        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e

def main():
    """Continuously run scripts in a loop, preventing ECS from stopping the task."""
    while True:
        try:
            print("Starting the video processing pipeline...")

            # Step 1: Fetch highlights
            run_script("fetch.py")
            print("Waiting for resources to stabilize...")
            time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

            # Step 2: Process the video
            run_script("process_one_video.py")
            print("Waiting for resources to stabilize...")
            time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

            # Step 3: Convert media with AWS MediaConvert
            run_script("mediaconvert_process.py")

            print("All scripts executed successfully. Sleeping for 6 hours before the next run...")
            time.sleep(21600)  # 6-hour sleep (adjust if needed)

        except Exception as e:
            print(f"Pipeline encountered an error: {e}. Retrying in 5 minutes...")
            time.sleep(300)  # Short sleep before retrying the loop

if __name__ == "__main__":
    main()
