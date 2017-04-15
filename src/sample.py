'''
The sample class for the imgprep script. One object of this class contains
three images of the sample. It also defines the methods used to process
the images.
'''
import os

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

        # Determining names
        for path in self.image_pathes:
            head, tail = os.path.split(path)
            name, extension = os.path.splitext(tail)
            self.image_names.append(name)
            self.image_extensions.append(extension)

        # Loading the images
        if self.image_count > 1:
            self.images = io.imread_collection(self.image_pathes)
        elif self.image_count = 1:
            self.images = io.imread(str(self.image_pathes))
        else:
            pass

        # TODO: Save metadata (magnification, scale, etc)
        # TODO: Maybe rotate the second polarized image by -45°

    def save_images(self, cropped=False):
        '''
        Method for saving the adjusted images.
        '''
        if cropped:
            ls = [self.image_names, self.image_extensions, self.cropped_images]
            for name, ext, img in zip(ls):
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
        self.box_dim = []
        self.box_coords = []

        # Iterate through images and detect each square
        for img in self.images:
            # Find all pixels greater than threshold (arbitrary)
            img_red_thresh = img[:, :, 0] > threshold
            # Marching squares algorithm to find contours
            img_contour = measure.find_contours(img_red_thresh,
                                                0, fully_connected='high')

            # Find index of the biggest contour
            i = [len(x) for x in img_contour].index(max([len(x) for x in img_contour]))

            # Find the coordinates
            x_points, y_points = zip(*img_contour[i])
            x_max = max(x_points)
            y_max = max(y_points)
            x_min = min(x_points)
            y_min = min(y_points)

            # The box dimensions
            self.box_dim.append(x_max - x_min, y_max - y_min)
            # The box coordinates
            self.box_coords.append(x_min, y_min)

    def crop(self):
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
