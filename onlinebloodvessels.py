# Import an image with scikit-image.
# NB: Blood vessel image from: https://www.fi.edu/heart/blood-vessels
from skimage import io
import numpy as np
import imagej

ij=imagej.init('/home/greebo/Desktop/Apps/Fiji.app')
url = 'https://www.congressis.ro/wp-content/uploads/2019/04/General_EduRes_Heart_BloodVessels_0.jpg'
img = io.imread(url)
img = np.mean(img, axis=2)

# show image
ij.py.show(img)
