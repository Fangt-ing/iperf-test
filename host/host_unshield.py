import subprocess

# Command lines to run
commands = 'iperf3 -s -V -p 5201'

subprocess.run(["cmd", "/c", "start", "cmd", "/k", commands], shell=True)