from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import pdb
import os
from PIL import Image, ImageDraw

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

@app.route("/sim-viral-spread")
def sim_viral_spread():
    population = int(request.args.get("population", ""))
    time = int(request.args.get("time", ""))
    initial = int(request.args.get("initial", ""))
    
    if(time < 5):
        return "Error, enter a time higher than 5"

    ls = viral_spread(population, time, initial)
    create_gif(ls)
    remove_files(ls)
    return send_file("out.gif", mimetype='image/gif')

def remove_files(ls):
    for im in ls[1]:
        os.remove(im)

def viral_spread(population,time,initial):
    grid_space=int(math.sqrt(population))
    grid=np.zeros((grid_space,grid_space))
    for i in range(0,initial):
        x0=np.random.randint(0,grid_space-1) 
        y0=np.random.randint(0,grid_space-1)
        grid[x0,y0]=1

    plt.imshow(grid, interpolation='none', vmin=0, vmax=1, aspect='equal')
    ax = plt.gca();
    ax.set_xticks(np.arange(0, grid_space, 1));
    ax.set_yticks(np.arange(0, grid_space, 1));
    ax.set_xticklabels(np.arange(1, grid_space+1, 1));
    ax.set_yticklabels(np.arange(1, grid_space+1, 1));

    plot_list=[]
    infectioncount=[]
    for a in range(0,time):
        for i in range(0,grid_space-1):
            for j in range(0,grid_space-1):
                if grid[i,j]==1:
                    x_step=0
                    y_step=0
                    x_step=i+np.random.randint(-1,2)
                    y_step=j+np.random.randint(-1,2)
                    grid[x_step,y_step]=1

    infectioncount.append(np.count_nonzero(grid))
    plt.figure()
    plt.imshow(grid, interpolation='none', vmin=0, vmax=1, aspect='equal')
    plt.savefig('plot{}.png'.format(str(a)))
    plot_list.append('plot{}.png'.format(str(a)))
    return [infectioncount[-1],plot_list]

def create_gif(ls):
    if(ls[0]==0):
        return
    images = []
    for im_path in ls[1]:
        im = Image.open(im_path)
    images.append(im)
    images[0].save('out.gif', save_all=True, append_images=images, duration=15, loop=1)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80)
