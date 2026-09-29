import pypsrp
import subprocess

# Install via terminal first: pip install pypsrp
from pypsrp.client import Client

myres = subprocess.run("hostname", capture_output=True, text=True).stdout
print(myres)

# Connect to a remote Windows machine
# with Client("windows-host.local", username="usename", password="", ssl=False) as client:
with Client("", username="", password="", ssl=False) as client :
# Execute script block remotely
    stdout, stderr, had_errors = client.execute_ps("Get-Service -Name wuauserv")
    print(stdout)