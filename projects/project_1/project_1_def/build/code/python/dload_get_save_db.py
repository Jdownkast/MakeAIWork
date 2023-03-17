from requests import get
from pandas import DataFrame

# Get data from rest server
# URL IS NOT STATIC > COMBINE WITH p1_dload_db
url = "http://localhost:8080/medish_centrum_randstad/api/netlify"
response = get(url)
dict_df = response.json()

# Put data in DataFrame and save as csv
df_mcr = DataFrame(dict_df["data"])
path_db = "../../csv/database/db_mcr.csv"
df_mcr.to_csv(path_db, index=False)
