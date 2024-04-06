# # import subprocess
# # import os
# # import platform

# # class IperfHost:
# #     def __init__(self, port=5201, udp=False):
# #         self.port = port
# #         self.udp = udp
# #         self.process = None

# #         # Check operating system and set iperf path accordingly
# #         if platform.system() == 'Windows':
# #              # Check CPU architecture for Windows
# #             if platform.architecture()[0] == '32bit':
# #                 self.iperf_path = '/iperf_bin/win32/iperf3.exe'
# #             elif platform.architecture()[0] == '64bit':
# #                 self.iperf_path = '/iperf_bin/win64/iperf3.exe'
# #         else:
# #             self.iperf_path = 'iperf'

# #     def start_server(self):
# #         if self.process and self.process.poll() is None:
# #             print("Server is already running.")
# #             return

# #         cmd = [self.iperf_path, '-s', '-p', str(self.port)]
# #         if self.udp:
# #             cmd.append('-u')
# #         try:
# #             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# #             print("Server started successfully.")
# #         except FileNotFoundError:
# #             print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")

# #     def stop_server(self):
# #         if self.process and self.process.poll() is None:
# #             self.process.terminate()
# #             print("Server stopped.")
# #         else:
# #             print("No server is running.")

# #     def get_server_status(self):
# #         if self.process and self.process.poll() is None:
# #             return "Server is running."
# #         else:
# #             return "Server is not running."

# # if __name__ == "__main__":
# #     iperf_host = IperfHost()
# #     iperf_host.start_server()
# #     print(iperf_host.get_server_status())
# #     input("Press Enter to stop the server...")
# #     iperf_host.stop_server()



# import subprocess
# import os
# import platform
# import glob

# class IperfHost:
#     def __init__(self, port=5201, udp=False):
#         self.port = port
#         self.udp = udp
#         self.process = None
#         self.iperf_path = self.find_iperf_path()

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

#     def start_server(self):
#         if not self.iperf_path:
#             print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")
#             return

#         if self.process and self.process.poll() is None:
#             print("Server is already running.")
#             return

#         # Start iperf server -s, -p 5201, -f M (Mbits)
#         cmd = [self.iperf_path, '-s', '-p', str(self.port),  '-f', 'M']
#         if self.udp:
#             cmd.append('-u')
#         try:
#             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             print("Server started successfully.")
#             print("Server PID: ", self.process.pid)
#         except FileNotFoundError:
#             print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")

#     def stop_server(self):
#         if self.process and self.process.poll() is None:
#             self.process.terminate()
#             print("Server stopped.")
#         else:
#             print("No server is running.")

#     def get_server_status(self):
#         if self.process and self.process.poll() is None:
#             return "Server is running."
#         else:
#             return "Server is not running."

# if __name__ == "__main__":
#     iperf_host = IperfHost()
#     iperf_host.start_server()
#     print(iperf_host.get_server_status())
#     input("Press Enter to stop the server...")
#     iperf_host.stop_server()


import subprocess
import os
import platform
import glob
import sys

class IperfHost:
    def __init__(self, port=5201, udp=False, output_file="output"):
        self.port = port
        self.udp = udp
        self.output_file = output_file
        self.process = None
        self.iperf_path = self.find_iperf_path()

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

    def start_server(self):
        if not self.iperf_path:
            print("Error: iperf not found. Please make sure iperf is installed and in your system PATH.")
            return

        if self.process and self.process.poll() is None:
            print("Server is already running.")
            return

        cmd = [self.iperf_path, '-s', '-p', str(self.port)]
        if self.udp:
            cmd.append('-u')
        if self.output_file:
            cmd.extend(['-o', self.output_file])
        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Server started successfully.")
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
    output_file = "output"
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    iperf_host = IperfHost(output_file=output_file)
    iperf_host.start_server()
    print(iperf_host.get_server_status())
    input("Press Enter to stop the server...")
    iperf_host.stop_server()
