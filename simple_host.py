import subprocess
import time
import datetime


def start_iperf_server(port):
    cmd = ['iperf3', '-s', '-V','-p', str(port)]
    subprocess.Popen(cmd)


if __name__ == "__main__":

    schedule_time = "20:12"

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            start_server = True
            break
        else:
            time.sleep(1)

    if start_server:
        start_iperf_server(5201)
        start_iperf_server(5202)
