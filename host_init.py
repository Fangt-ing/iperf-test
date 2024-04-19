import subprocess
import time
import datetime

if __name__ == "__main__":

    schedule_time = "21:12"
    python_files = ["host/host_shield.py", "host/host_unshield.py"]

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            for python_file in python_files:
                    subprocess.run(["python", python_file])
            break
        else:
            time.sleep(1)
