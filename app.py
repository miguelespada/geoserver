from flask import Flask
from flask import jsonify, request
import time
import csv

from PIL import Image
from pyproj import Proj, transform

app = Flask(__name__)

img = Image.open("crop_20000_10000.png")
dX = 20000
dY = 10000

colores = {}

with open('clc_legend.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        colores[row[3]] =  (row[1], row[2])

Origin = (-2699875.0000000000, 5499875.0000000000)

inProj = Proj(init='EPSG:4326')
outProj = Proj(init='EPSG:3035')

def getPixel((lat, lon)):
    coord = transform(inProj,outProj,lon,lat)
    x = int(((coord[0] - Origin[0]) / 250) - dX)
    y = int(abs(((coord[1] - Origin[1]) / 250 )) - dY)
    return img.getpixel((x, y))

@app.route('/<coords>')
def index(coords):
   tokens = coords.split(',')
   coords = float(tokens[0]), float(tokens[1])
   color =  getPixel(coords)
   colorString =  "%03d-%03d-%03d" % color
   description = colores[colorString]
   d = {"r" : color[0],
        "g": color[1],
        "b": color[2],
        "code": description[0],
        "type": description[1], 
         "isNature": (int(description[0]) > 200)}  
   return jsonify(d)
 

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)