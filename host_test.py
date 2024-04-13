import subprocess
import platform
import sys
import time
import datetime

class IperfHost:
    def __init__(self, port=5201, udp=False, interval=1, output_file='output'):
        self.port = port
        self.udp = udp
        self.process = None
        self.iperf_path = 'iperf3'
        self.output_file = output_file
        self.interval = interval

    def start_server(self):
        if self.process and self.process.poll() is None:
            print("Server is already running.")
            return

        cmd = ['iperf3', '-s', '-p', str(self.port), '-i', str(self.interval), '-J']
        if self.udp:
            cmd.append('-u')
        cmd.append('--logfile')
        cmd.append(f'output/{self.output_file}.json')
        try:
            self.process = subprocess.Popen(cmd)
            print("Server started successfully.")
            print("Command line inputs:", ' '.join(cmd))
        except FileNotFoundError:
            print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")

    def stop_server(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            print("Server stopped.")
        else:
            print("No server is running.")

    def get_server_status(self):
        if self.process and self.process.poll() is None:
            return "Server is running."
        else:
            return "Server is not running."


if __name__ == "__main__":
    # output_file_name = 'hostJs'
    output_file_name = 'db0/f24-ni-ch1-host'

    if len(sys.argv) > 1:
        output_file_name = sys.argv[1]

    # Replace 'script.py' with the name of the Python script you want to run
    schedule_time = "15:35"

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            iperf_host = IperfHost(output_file=output_file_name)
            iperf_host.start_server()
            print(iperf_host.get_server_status())
            input("Press Enter to stop the server...")
            iperf_host.stop_server()
            break
        else:
            time.sleep(1)
