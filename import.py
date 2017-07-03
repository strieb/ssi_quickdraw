
import struct
from struct import unpack
from urllib.request import urlopen 
from urllib.request import urlopen
import urllib.parse
from pathlib import Path



def read_categories():
    with open('categories.txt', 'r') as f:
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
    samples_info.write("""<?xml version="1.0" ?>
<samples ssi-v="3">
    <info ftype="ASCII" size="50" missing="false" garbage="0" />
    <streams>
        <item path="numbers_train.samples.#0" />
    </streams>
    <classes>
""")
    stream_info.write("""<?xml version="1.0" ?>
<stream ssi-v="2">
    <info ftype="ASCII" sr="50.000000" dim="1" byte="1" type="BYTE" delim=" " />
    <meta />
""")
    categories = read_categories()
    c = 0
    for category in categories:
        drawings = unpack_drawings(category)
        n = 0
        b = 0
        for drawing in drawings:
            samples_data.write('0 '+str(c)+ ' 0 0\n')
            stream_info.write('    <chunk from="0" to="1" byte="'+str(b)+'" num="256"/>\n')
            n += 1
            b += 256
            if n == 1000:
                break
        samples_info.write('        <item name="'+category+'" size="'+str(n)+'" />\n')
        c += 1            
    samples_info.write("""    </classes>
    <users>
        <item name="user" size="30000" />
    </users>
</samples>""")
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

        

write_samples("train")


