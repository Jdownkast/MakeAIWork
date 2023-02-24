"""Project 1: MiW (2023); Get data from
 database 'medisch_centrum_randstad'"""

import os
from requests import get
from pandas import DataFrame
import subprocess

# Boot rest server
home = os.getcwd()
rs_path = os.path.join(home, "projects/project_1/rest_server")
print(rs_path)
# subprocess.Popen(f"{rs_path}/start_rest_server.sh")

# Get data from rest server
url = "http://localhost:8080/medish_centrum_randstad/api/netlify"
response = get(url)
dict_df = response.json()

# Put data in DataFrame
df_mcr = DataFrame(dict_df["data"])
print('Database "Medisch Centrum Randstad" loaded.')
print(df_mcr.head())
