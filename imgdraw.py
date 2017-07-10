
import numpy as np
import math

def line(img, x1,y1,x2,y2):
	len = math.hypot(x1-x2 , y1-y2)
	samples = (int) (len * 10)
	for i in range(0, samples + 1):
		img[int((x2-x1)*(i/samples)+x1),int((y2-y1)*(i/samples)+y1)] += 1
	print(len)
	

img = np.zeros((10, 10), dtype=np.uint8)
line(img, 3, 8, 5, 5)
line(img, 5, 5, 9, 9)
print(img)
