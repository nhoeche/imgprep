'''
The sample class for the imgprep script. One object of this class contains
three images of the sample. It also defines the methods used to process
the images.
'''

import numpy as np
import skimage
import skimage.io as io
import skimage.measure as measure


class Sample(object):
    '''
    Class for a sample. Including microscopy images and methods for editing.

    -=VARIABLES=-
    sample_name:    Name of the Sample
    image_count:    Number of associated images
    image_pathes:   Full pathes of the image-files
    images:         Array of microscopy-image-files

    box_dim:        Dimensions of the box (ROI)
    box_coords:     Coordinations of the top-left corner of the box (ROI)
    '''
    def __init__(self, sample_name):
        '''
        Creates instances of the Sample class and sets initial variables.
        '''
        self.sample_name = sample_name
        self.image_pathes = []
        self.image_names = []
        self.image_count = 0
        self.images = []

    def load_images(self, filenames):
        '''
        Loads microscope images of the sample as numpy arrays and saves the
        image metadata. Make sure to have filenames and image_pathes set so
        load the images.
        '''
        # Setting up variables
        self.image_pathes = filenames
        self.image_count = len(self.image_pathes)
        self.image_names = [None] * self.image_count
        self.image_extensions = [None] * self.image_count
        self.images = [None] * self.image_count

        # Determining names
        for i, img in enumerate(self.image_pathes):
            _, name = img.rsplit('/')
            name, extension = name.split('.')
            self.image_names[i] = name
            self.image_extensions[i] = extension

        # Loading the images
        if self.image_count > 1:
            self.images = io.imread_collection(self.image_pathes)
        else:
            self.images = io.imread(str(self.image_pathes))

        # TODO: Save metadata (magnification, scale, etc)
        # TODO: Maybe rotate the second polarized image by -45°

    def save_images(self, cropped=False):
        '''
        Method for saving the adjusted images.
        '''
        if cropped:
            for i, img in enumerate(self.cropped_images):
                name = self.image_names[i]
                ext = self.image_extensions[i]
                filename = '{}_cropped.{}'.format(name, ext)
            io.imsave(filename, img)
        else:
            pass

    def detect_square(self, threshold=150):
        '''
        Detects the square in the sample image. Determines box dimensions and
        coordinates.
        '''
        # Setting up the box variables
        self.box_dim = np.zeros((self.image_count, 2), dtype=np.int8)
        self.box_coords = np.zeros((self.image_count, 2), dtype=np.int8)

        # Iterate through images and detect each square
        for index, img in enumerate(self.images):
            # Find all pixels greater than threshold (arbitrary)
            img_red_thresh = img[:, :, 0] > threshold
            # Marching squares algorithm to find contours
            img_contour = measure.find_contours(img_red_thresh,
                                                0, fully_connected='high')

            # Find index of the biggest contour
            i = [len(x) for x in img_contour].index(max([len(x) for x in img_contour]))

            # Instantiate the largest x- and y-coordinates for each coordinate
            x_max = 0
            y_max = 0
            x_min = img_contour[i][0][0]
            y_min = img_contour[i][0][0]

            # Iteratively pick out the max and min values and assigns them
            for point in img_contour[i]:
                if point[0] > x_max:
                    x_max = point[0]
                if point[0] < x_min:
                    x_min = point[0]
                if point[1] > y_max:
                    y_max = point[1]
                if point[1] < y_min:
                    y_min = point[1]

            # The box dimensions
            self.box_dim[index] = (x_max - x_min, y_max - y_min)
            # The box coordinates
            self.box_coords[index] = (x_min, y_min)

    def crop(self):
        self.cropped_images = [None] * self.image_count

        # Iterate over images and crop
        for index, img in enumerate(self.images):
            # Setting up coordinates
            left = self.box_coords[index][0]
            right = left + self.box_dim[index][0]

            top = self.box_coords[index][1]
            bot = top + self.box_dim[index][1]

            # Cropping
            self.cropped_images[index] = img[left:right, top:bottom, :]

        # TODO: Recognize the Magnification and calculate scale-bar dimensions
        # TODO: Crop the images and place them next to each other
        # TODO: Create three scale-bars and insert them into the images
        # TODO: Recognize the width of the border
