"""Project 1: MiW (2023); Get data from
 database 'medisch_centrum_randstad'"""

import os
from requests import get
from pandas import DataFrame
import signal
import subprocess

# Set paths & commands
bash_dir = "C:/Program Files/Git/bin"
start_bash = f"{bash_dir}/bash.exe"

home = os.getcwd()
server_dir = os.path.join(home, "projects/project_1/rest_server/").replace("\\", "/")
start_server = "./db_serverstart.sh"
get_pid = 'echo "$!"'

bash_command = f"cd {server_dir} && {start_server} & {get_pid}"
cmd_command = [start_bash, "-c", bash_command]
# cmd_command = f"""start "" "{start_bash}" -c "{bash_command}" """
# cmd_command = f"""start "" "{start_bash}" -c "which python && sleep 20" """

# Boot rest server
output = subprocess.Popen(cmd_command, shell=True)


# Get data from rest server
url = "http://localhost:8080/medish_centrum_randstad/api/netlify"
response = get(url)
dict_df = response.json()

# Put data in DataFrame
df_mcr = DataFrame(dict_df["data"])
print('Database "Medisch Centrum Randstad" loaded.')
print(df_mcr.head())

# ans = server.poll()
# server.send_signal(signal.SIGINT)
# server.terminate()
# server.kill()

print(output)
