import skimage
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

img = io.imread('sample_images/Hofer2_63x_gekreuzt_evtl-coccolithB2.jpg')

np.shape(img)   # Image as numpy 3d-Array (x*y, z=3 RGB)
plt.imshow(img)
