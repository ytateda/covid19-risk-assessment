def return_active_cases(country_name):
  import pandas as pd
  import requests
  from bs4 import BeautifulSoup

  req = requests.get("https://www.worldometers.info/coronavirus/")
  soup = BeautifulSoup(req.content)

  data = list(map(lambda x: list(map(lambda y: y.text, x.select("td, th"))),soup.select("table#main_table_countries_today tr")))

  df = pd.DataFrame(data)
  df.columns = df.iloc[0]
  df = df.drop(0, axis=0)
  df = df.fillna(0)

  i = df.loc[df['Country']==country_name].index[0]
  active_cases = df['ActiveCases'][i]

  return active_cases
