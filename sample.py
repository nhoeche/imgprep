import skimage
import numpy as np

'''
The sampe class for the imgprep script. One object of this class contains three
images of the same sample. It also defines the methods used to process the
images.
'''


class Sample:

    def __init__(self):
        self.filenames = []
        self.pathes = []
        self.images = []

    def load_images(self):
        self.images = [i for i in range(len(self.filenames))]
        for i, (filename, path) in enumerate(zip(self.filenames, self.pathes)):
            self.images[i] = skimage.io.imread('{}/{}'.format(path, filename))
            self.images[i] = skimage.img_as_float(self.images[i])

        # TODO: Save metadata and image objects into numpy array / pandas
        #       frame
        # TODO: Rotate the second polarized image by -45°

    def square_detect(image):
        # Copypasted, functionality not guaranteed
        # cols = (image[..., 0] == 255).sum(0)
        # left = cols.argsort()[-2:].min()
        # right = cols.argsort()[-2:].max()
        pass

    # TODO: Recognize the Magnification and calculate scale-bar dimensions
    # TODO: Recognize the Red square coordinates
    # TODO: Crop the images and place them next to each other
    # TODO: Create three scale-bars and insert them into the images
