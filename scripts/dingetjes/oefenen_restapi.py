import http.client
import pandas as pd

year = 2022
conn = http.client.HTTPSConnection("ergast.com")

headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
}

payload = ""

conn.request("GET", f"/api/f1/{year}/driverStandings.json", payload, headersList)
response = conn.getresponse()
result = response.read()

result = result.decode("utf-8")

df = pd.read_json(result)
# df = pd.json_normalize(result, record_path="StandingsTable")
print(df)
