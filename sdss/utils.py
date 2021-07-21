from urllib.request import urlopen, urlretrieve
import matplotlib.pyplot as plt
import pandas as pd
import binascii, io
from PIL import Image
import numpy as np

def sql2df(script):
    BASE = "http://skyserver.sdss.org/dr16/SkyServerWS/SearchTools/SqlSearch?cmd="
    script = ' '.join(script.strip().split('\n'))
    url = BASE+script.replace(' ', '%20') + '&format=csv'
    r = urlopen(url).read().decode('utf-8')
    lines = r.splitlines()
    col = lines[1].split(',')
    data_lines = [i.split(',') for i in lines[2:]]
    return pd.DataFrame(data_lines, columns=col)

def binimg2array(img_raw):
    img_raw = img_raw[2:]
    img_b = binascii.a2b_hex(img_raw)
    img = Image.open(io.BytesIO(img_b))
    data = np.array(img)
    return data

def img_cutout(ra, dec, scale, width, height, opt, query):
    BASE = "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?"
    PAR = f"ra={ra}&dec={dec}&scale={scale}&width={width}&height={height}"
    OPT = "&opt="+opt if opt !='' else ''
    QRY = "&query="+query if query!='' else ''
    url = BASE + PAR + OPT + QRY
    data = plt.imread(urlopen(url), format='jpeg')
    return data

def show_spect(specObjID, figsize=(15,20)):
    url = f"http://skyserver.sdss.org/dr16/en/get/SpecById.ashx?id={specObjID}"
    data = plt.imread(urlopen(url), format='jpeg')
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(data)
    plt.show()

def show_object(objID, scale=0.1, width=300, height=300, figsize=(10,10)):
    script = f"SELECT TOP 1 ra,dec FROM PhotoObj WHERE objID={objID}"
    df = sql2df(script)
    ra, dec = df['ra'].iloc[0], df['dec'].iloc[0]
    data = img_cutout(ra, dec, scale=scale, width=width, height=height, opt='', query='')
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(data)
    plt.show()