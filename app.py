from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas as gpd
import os 
import contextily as ctx
import matplotlib.pyplot as plt

regioni = gpd.read_file("Regioni/Reg01012023_WGS84.dbf")
regioni3857 = regioni.to_crs(3857)

@app.route('/')
def home():
    reg = list(regioni["DEN_REG"])
    reg.sort()
    return render_template("home.html", lista = reg)

@app.route('/esercizio', methods = ["GET"])
def esercizio():
    regione = request.args.get("regione")
    regione_selezionata = regioni3857[regioni3857["DEN_REG"] == regione.capitalize()]
    ax = regione_selezionata.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "mappa.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("mappa.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)