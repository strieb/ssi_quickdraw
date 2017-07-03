import matplotlib.pyplot as plt
import numpy as np
import time

def draw(image):

    '''Convert strokes to an image and plot with matplotlib.'''
    img_arr = np.array(image)
    
    fig = plt.figure(frameon=False, figsize=(1, 1), dpi=32)
    
    for i in range(len(img_arr)):
        axis = fig.add_subplot(111)
        axis.set_axis_off()
        axis.plot(img_arr[i][0], [(255 - k) for k in img_arr[i][1]], c='b')
    fig.savefig('test.png')
    plt.show(block=False)
    time.sleep(2)
    plt.close(fig)
    del fig
   
   
'''Uncomment for test purpose'''

image = [((88, 86, 82, 70, 56, 30, 9, 2, 0, 14, 46, 152, 190, 225, 242, 254, 
           255, 251, 203, 188, 181, 173, 175),
           (1, 66, 82, 98, 106, 113, 126, 139, 165, 178, 188, 190, 183, 170, 153, 126,
           103, 96, 76, 66, 56, 36, 0)), ((48, 50), (174, 169))]
           
image2 = [((95, 8, 0, 3, 19, 52, 90, 133, 202, 231, 238, 235), 
           (0, 193, 230, 240, 245, 237, 234, 237, 250, 252, 253, 255)), 
          ((90, 74, 58, 91, 108, 116, 124, 126, 129), 
           (227, 222, 230, 193, 190, 191, 199, 232, 234)), 
          ((173, 178, 185, 201, 209, 217, 221, 221, 216), 
           (221, 204, 194, 183, 181, 185, 195, 214, 252))]
           
draw(image)
#draw(image2)