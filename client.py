# import subprocess
# import os
# import platform
# import sys

# class IperfClient:
#     def __init__(self, host_ip, host_port=5201, udp=False, output_file='output'):
#         self.host_ip = host_ip
#         self.host_port = host_port
#         self.udp = udp
#         self.process = None
#         self.iperf_path = self.find_iperf_path()
#         self.output_file = output_file

#     def find_iperf_path(self):
#         # Check operating system and set iperf path accordingly
#         iperf_executable = 'iperf3'
#         if platform.system() == 'Windows':
#             iperf_executable = 'iperf3.exe'
#         # Search for iperf3.exe in subfolders
#         iperf_path = None
#         for root, dirs, files in os.walk('.'):
#             for name in files:
#                 if name == iperf_executable:
#                     iperf_path = os.path.join(root, name)
#                     break
#             if iperf_path:
#                 break
#         return iperf_path

#     def start_client(self):
#         if not self.iperf_path:
#             print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")
#             return

#         cmd = [self.iperf_path, '-c', self.host_ip, '-p', str(self.host_port), '-V', '-f', 'M']
#         if self.udp:
#             cmd.append('-u')
#         cmd.append('--logfile')
#         cmd.append(f'output/{self.output_file}.log')
#         try:
#             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             print("Client started successfully.")
#             print("Command line inputs:", ' '.join(cmd))
#         except FileNotFoundError:
#             print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")

#     def stop_client(self):
#         if self.process and self.process.poll() is None:
#             self.process.terminate()
#             print("Client stopped.")
#         else:
#             print("No client is running.")

#     def get_client_status(self):
#         if self.process and self.process.poll() is None:
#             return "Client is running."
#         else:
#             return "Client is not running."

# if __name__ == "__main__":
#     output_file_name = 'client'
#     if len(sys.argv) > 1:
#         output_file_name = sys.argv[1]

#     host_ip = 'localhost'
#     iperf_client = IperfClient(host_ip, output_file=output_file_name)
#     iperf_client.start_client()
#     print(iperf_client.get_client_status())
#     input("Press Enter to stop the client...")
#     iperf_client.stop_client()

import subprocess
import os
import platform
import sys
import time

class IperfClient:
    def __init__(self, host_ip, host_port=5201, udp=False, output_file='output', measurement_duration=60):
        self.host_ip = host_ip
        self.host_port = host_port
        self.udp = udp
        self.process = None
        self.iperf_path = self.find_iperf_path()
        self.output_file = output_file
        self.measurement_duration = measurement_duration

    def find_iperf_path(self):
        # Check operating system and set iperf path accordingly
        iperf_executable = 'iperf3'
        if platform.system() == 'Windows':
            iperf_executable = 'iperf3.exe'
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

        cmd = [self.iperf_path, '-c', self.host_ip, '-p', str(self.host_port), '-V', '-f', 'M']
        if self.udp:
            cmd.append('-u')
        cmd.append('-t')
        cmd.append(str(self.measurement_duration))  # Set measurement duration
        cmd.append('--logfile')
        cmd.append(f'output/{self.output_file}.log')
        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Client started successfully.")
            print("Command line inputs:", ' '.join(cmd))
            # Wait for measurement duration and then stop the client
            time.sleep(self.measurement_duration)
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
            return "Client is running."
        else:
            return "Client is not running."

if __name__ == "__main__":
    output_file_name = 'client'
    if len(sys.argv) > 1:
        output_file_name = sys.argv[1]

    host_ip = 'localhost'
    # measurement_duration = int(input("Enter measurement duration in seconds: "))
    iperf_client = IperfClient(host_ip, output_file=output_file_name)
    iperf_client.start_client()
    print(iperf_client.get_client_status())
