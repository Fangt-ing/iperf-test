import subprocess
import time

def start_iperf_server(port):
    cmd = ['iperf3', '-s', '-p', str(port)]
    subprocess.Popen(cmd)

if __name__ == "__main__":

    start_iperf_server(5201)
    start_iperf_server(5202)

    # Add a delay to ensure the servers have enough time to start
    time.sleep(2)
