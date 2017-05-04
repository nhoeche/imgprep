'''
The sample class for the imgprep script. One object of this class contains
three images of the sample. It also defines the methods used to process
the images.
'''
import os

import skimage
import skimage.io as io
import skimage.measure as measure


class Sample(object):
    '''
    Class for a sample. Including microscopy images and methods for editing.
    '''
    def __init__(self, sample_name):
        '''
        Creates instances of the Sample class and sets initial variables.
        '''
        self.sample_name = sample_name
        self.image_list = []
        self.image_count = 0

        self.cropped_images = []

    def load_images(self, filenames):
        '''
        Loads a microscope images as numpy array and saves the image metadata.
        Make sure to have filenames and pathes set so load the images.
        '''
        self.image_count = len(filenames)

        for filename in filenames:
            self.image_list.append(Image(filename))

        # TODO: Save metadata (magnification, scale, etc)
        # TODO: Maybe rotate the second polarized image by -45°

    def save_images(self, cropped=False):
        '''
        Method for saving the adjusted images.
        '''
        if cropped:
            # Iterate over images
            for img, cropped in zip(self.image_list, self.cropped_images):
                filename = '{}_cropped.{}'.format(img.name, img.extension)
                io.imsave(filename, cropped)
        else:
            print("Error: Cannot save image. No changes have been made.")
            pass

    def crop(self):
        '''
        Iterate over images, detect squares and crop
        '''
        for img in self.image_list:
            # Detecting the square (ROI)
            img.detect_roi()

            # Setting up coordinates
            left = img.roi_coords[0]
            right = left + img.roi_dim[0]
            top = img.roi_coords[1]
            bot = top + img.roi_dim[1]
            # Cropping
            self.cropped_images.append(img.image[left:right, top:bot, :])

        # TODO: Recognize the Magnification and calculate scale-bar dimensions
        # TODO: Crop the images and place them next to each other
        # TODO: Create three scale-bars and insert them into the images
        # TODO: Recognize the width of the border


class Image(object):
    '''
    Subclass of the sample class for images of each sample. It contains all in-
    formation concerning the images, as well as the image-files themselves.
    Methods performing on a single image are stored here.
    '''
    def __init__(self, filename):
        '''
        Instantiates an image object, loads the image and sets up the variables
        '''
        # Name
        self.path = filename
        head, tail = os.path.split(self.path)
        self.name, self.extension = os.path.splitext(tail)

        # File
        self.image = io.imread(self.path)

        # ROI parameters
        self.roi_dim = []
        self.roi_coords = []

    def detect_roi(self, threshold=150):
        '''
        Detects the square in the sample image. Determines ROI dimensions and
        coordinates.
        '''
        # Find all pixels greater than threshold (arbitrary)
        img_red_thresh = self.image[:, :, 0] > threshold

        # Marching squares algorithm to find contours
        img_contours = measure.find_contours(img_red_thresh,
                                             0, fully_connected='high')

        # Find index of the biggest contour
        i = [len(x) for x in img_contours].index(max([len(x) for x in img_contours]))

        # TODO: Add is_square method to check whether the ROI is a square

        # Find the coordinates
        x_points, y_points = zip(*img_contours[i])
        x_max = int(max(x_points))
        y_max = int(max(y_points))
        x_min = int(min(x_points))
        y_min = int(min(y_points))

        # The ROI dimensions
        self.roi_dim = [x_max - x_min, y_max - y_min]

        # The ROI coordinates
        self.roi_coords = [x_min, y_min]
