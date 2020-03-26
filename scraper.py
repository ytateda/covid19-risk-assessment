import pandas as pd
import requests
from bs4 import BeautifulSoup

req = requests.get("https://www.worldometers.info/coronavirus/")
soup = BeautifulSoup(req.content)

data = list(map(lambda x: list(map(lambda y: y.text, x.select("td, th"))),soup.select("table#main_table_countries_today tr")))

df = pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.drop(0, axis=0)
df.to_csv("covid19.csv")
