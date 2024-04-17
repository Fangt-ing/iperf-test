import subprocess
import os
import platform
import sys
import time
import datetime


class IperfClient:
    def __init__(self, host_ip, host_port=5201, udp=False, upload=False, interval=1, output_file='output', measurement_duration=160):
        self.host_ip = host_ip
        self.host_port = host_port
        self.interval = interval
        self.udp = udp
        self.upload = upload
        self.process = None
        self.iperf_path = self.find_iperf_path()
        self.output_file = output_file
        self.measurement_duration = measurement_duration

    def find_iperf_path(self):
        # Check operating system and set iperf path accordingly
        iperf_executable = 'iperf3'
        if platform.system() == 'Windows':
            iperf_executable = 'iperf3.exe'
        elif platform.system() == 'Linux':
            return iperf_executable
        # Search for iperf3.exe in subfolders
        iperf_path = None
        for root, dirs, files in os.walk('.'):
            for name in files:
                if name == iperf_executable:
                    iperf_path = os.path.join(root, name)
                    break
            if iperf_path:
                break
        return iperf_path

    def start_client(self):
        if not self.iperf_path:
            print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")
            return

        cmd = [self.iperf_path, '-c', self.host_ip, '-p', str(self.host_port), '-i', str(self.interval),'-J', '-R']
        if self.udp:
            cmd.append('-u')
        if self.upload:
            cmd.pop(-1)
        cmd.append('-t')
        cmd.append(str(self.measurement_duration))  # Set measurement duration
        cmd.append('--logfile')
        cmd.append(f'output/{self.output_file}.json')
        # cmd.append(f'--get-server-output')
        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Client started successfully.")
            print("Command line inputs:", ' '.join(cmd))
            # Wait for measurement duration and then stop the client
            time.sleep(self.measurement_duration+2)
            self.stop_client()
        except FileNotFoundError:
            print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")

    def stop_client(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            print("Client stopped.")
        else:
            print("No client is running.")

    def get_client_status(self):
        if self.process and self.process.poll() is None:
            if self.upload:
                return "Client is running in upload mode."
            else:
                return "Client is running in download mode."
        else:
            return "Client is not running."

if __name__ == "__main__":
    # output_file_name = 'db0/f24-coi-ch1-unshield'
    # output_file_name = 'db0/f24-aci-ch6-1-unshield'
    output_file_name = 'db0/f24-coi-ch6-unshield'

    if len(sys.argv) > 1:
        output_file_name = sys.argv[1]

    # host_ip = 'localhost'
    host_ip = '192.168.0.104'

    schedule_time = "20:13"
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            iperf_client = IperfClient(host_ip, output_file=output_file_name+str("-download"))
            iperf_client.start_client()
            print(iperf_client.get_client_status())
            print("--------------------\n")

            iperf_client = IperfClient(host_ip, upload=True,output_file=output_file_name+str("-upload"))
            iperf_client.start_client()
            print(iperf_client.get_client_status())
            break
        else:
            time.sleep(1)
