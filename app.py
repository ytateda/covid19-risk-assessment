from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import pdb

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/get-active-cases")
def get_active_cases():
    country_name = str(request.args.get("country", ""))
    df = get_covid_df()
    i = df.loc[df['Country,Other']==country_name].index[0]
    active_cases = df['ActiveCases'][i]

    return jsonify(cases=active_cases)


@app.route("/get-countries")
def get_countries():
    df = get_covid_df()
    return jsonify(countries=df['Country,Other'].values.tolist())

def get_covid_df():
    req = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(req.content)

    data = list(map(lambda x: list(map(lambda y: y.text, x.select("td, th"))),soup.select("table#main_table_countries_today tr")))

    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.drop(0, axis=0)
    df = df.fillna(0)
    return df

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80)
