'''
The sample class for the imgprep script. One object of this class contains
three images of the sample. It also defines the methods used to process
the images.
'''

import skimage
import skimage.io
from PIL import Image


class Sample(object):

    def __init__(self, sample_name):
        '''
        Creates instances of the Sample class.
        '''

        self.name = sample_name
        self.image_paths = []
        self.images = []


    def load_images(self):
        '''
        Loads microscope images of the sample as numpy arrays and saves the
        image metadata. Make sure to have filenames and image_pathes set so
        load the images.
        '''
#        self.images = [None] * self.numberofimages

#        if self.numberofimages > 1:
#            self.images = skimage.io.imread_collection(self.image_paths)
#        else:
#            self.images = skimage.io.imread(str(self.image_paths))

        self.image = Image.open(self.image_paths)

        # TODO: Save metadata
        # TODO: Maybe rotate the second polarized image by -45°

    def detect_square(self):
        im = self.image
        px = self.image.load()

        xlist = []
        ylist = []
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                # Looks for R>236 G<40 color values and stores them in a list.
                if px[x, y][0] > 239 and px[x, y][1] < 40:
                    xlist.append(x)
                    ylist.append(y)

        # Inside corners of the bounding box
        self.xl = min(xlist)+8  # Left
        self.xr = max(xlist)-8  # Right
        self.yt = min(ylist)+8    # Top
        self.yb = max(ylist)-8    # Bottom
        self.cropbox = [self.xl, self.yt, self.xr, self.yb]


    # TODO: Recognize the Magnification and calculate scale-bar dimensions
    # TODO: Crop the images and place them next to each other
    # TODO: Create three scale-bars and insert them into the images
    # TODO: Recognize the width of the border
