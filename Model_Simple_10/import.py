
import struct
from struct import unpack
from urllib.request import urlopen 
from urllib.request import urlopen
import urllib.parse
from pathlib import Path
import numpy as np
import math
import cv2

np.set_printoptions(threshold=np.nan)

def read_categories():
    with open('categories_10.txt', 'r') as f:
        categories = f.readlines()
    categories = [x.strip() for x in categories]
    return categories

def write_samples(filename):
    with open(filename+".samples","w") as samples_info:
        with open(filename+".samples~","w") as samples_data:
            with open(filename+".samples.#0.stream","w") as stream_info:
                with open(filename+".samples.#0.stream~","wb") as stream_data:
                    read_and_write(samples_info,samples_data,stream_info,stream_data)
                   
def read_and_write(samples_info,samples_data,stream_info,stream_data):
    categories = read_categories()
    samples_info.write("""<?xml version="1.0" ?>
<samples ssi-v="3">
    <info ftype="ASCII" size='"""+str(len(categories) * N) +"""' missing="false" garbage="0" />
    <streams>
        <item path="train.samples.#0" />
    </streams>
    <classes>
""")
    stream_info.write("""<?xml version="1.0" ?>
<stream ssi-v="2">
    <info ftype="BINARY" sr="1.000000" dim="1024" byte="4" type="FLOAT" delim=" " />
    <meta />
""")
    b = 0
    drawings = []
    for c in range(len(categories)):
        category = categories[c]
        drawings.append(unpack_drawings(category))
        samples_info.write('        <item name="'+category+'" size="'+str(N)+'" />\n')        
    samples_info.write("""    </classes>
    <users>
        <item name="user" size='"""+str(len(categories) * N) +"""' />
    </users>
</samples>""")
    
    for n in range(SKIP):
        for c in range(len(categories)):
            
            while True:
                drawing = next(drawings[c])
                if drawing['recognized']:
                    break
        
        
    for n in range(N):
        print(str(n))
        for c in range(len(categories)):
            while True:
                drawing = next(drawings[c])
                if drawing['recognized']:
                    break
            category = categories[c]
            img = np.zeros((32, 32), dtype=np.float32)
            samples_data.write('0 '+str(c)+ ' 0 0\n')
            stream_info.write('    <chunk from="0" to="1" byte="'+str(b)+'" num="1"/>\n')
            b += 4096
            img_arr =  np.array(drawing['image'])
            for i in range(len(img_arr)):
                for j in range(len(img_arr[i][0]) - 1):
                    x1 = int( img_arr[i][0][j] / 8)
                    y1 = int( img_arr[i][1][j] / 8)
                    x2 = int( img_arr[i][0][j + 1] / 8)
                    y2 = int( img_arr[i][1][j + 1] / 8)
                    line(img, x1,y1, x2, y2,1)
            stream_data.write(struct.pack('f'*1024,*img.flat))
    stream_info.write("</stream>")
			

    

def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    countrycode, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        image.append((x, y))

    return {
        'key_id': key_id,
        'countrycode': countrycode,
        'recognized': recognized,
        'timestamp': timestamp,
        'image': image
    }


def line(img, x1,y1,x2,y2,col):
	l = math.hypot(x1-x2 , y1-y2)
	if l == 0:
	    return
	samples = (int) (l * 5)
	for i in range(0, samples + 1):
            img[int((x2-x1)*(i/samples)+x1),int((y2-y1)*(i/samples)+y1)] += col / 5
	    
def unpack_drawings(filename):
    path = "binaries/"+filename+".bin";
    my_file = Path(path)
    if not my_file.exists():
        response = urlopen('https://storage.googleapis.com/quickdraw_dataset/full/binary/'+urllib.parse.quote(filename)+".bin")
        CHUNK = 16 * 1024
        with open(path, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

    
    with open(path, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break

        
SKIP = 100
N = 5000
write_samples("train")

SKIP = 0
N = 100
write_samples("test")


