"""
The Sample and Image class for the imgprep script.

The Sample class defines the methods used to process one sample and
contains all information about it (including multiple images).
The image class contains one of the multiple images of the sample, their
metadata, and methods processing the single images.
"""
import re
import os
import tempfile

import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

import pandas as pd

import skimage.io as io
import skimage.measure as measure


class Sample(object):
    """Class for samples. Including images and methods for processing."""

    def __init__(self, sample_name, verbose=False):
        """Create instances of the Sample class and sets initial variables."""
        if verbose:
            print('Generating a new sample named {}'.format(sample_name))
        self.sample_name = sample_name
        self.image_list = []
        self.image_count = 0

        self.edited_image_list = []

    def load_images(self, filepaths, verbose=False):
        """
        Load a microscope images as numpy array and saves the image metadata.

        Make sure to have filenames and paths set so load the images.
        """
        if verbose:
            print('Loading the specified images..')

        self.image_count = len(filepaths)

        for image in filepaths:
            self.image_list.append(Image(image, verbose=verbose))

        if verbose:
            print('Images loaded.')
        # TODO: Save metadata (magnification, scale, etc)
        # TODO: Maybe rotate the second polarized image by -45°

    def save_images(self, verbose=False):
        """Save the processed images of the sample."""
        if verbose:
            print('Saving the processed image..')

        # Iterate over images
        for edited_img in self.edited_image_list:
            filepath = os.path.join(edited_img.dir_name, edited_img.filename)
            io.imsave(filepath, edited_img.image)

        if verbose:
            print('Image saved.')

    def init_editing(self):
        """Initialize an array for the edited images and calculate filename."""
        for img in self.image_list:
            # New filename
            new_filename = '{}_edited{}'.format(img.name, img.extension)
            edit_filepath = os.path.join(img.dir_name, new_filename)
            edit_img = Image(edit_filepath, image=img.image, load=False)
            self.edited_image_list.append(edit_img)

    def crop(self, verbose=False):
        """Iterate over the images, detect the ROI and crop."""
        if verbose:
            print('Starting the cropping process..')

        for img, edit_img in zip(self.image_list, self.edited_image_list):
            # Detecting the square (ROI)
            img.detect_roi()
            edit_img.roi_coords = img.roi_coords
            edit_img.roi_dim = img.roi_dim

            # Setting up coordinates
            left = img.roi_coords[0]
            right = left + img.roi_dim[0]
            top = img.roi_coords[1]
            bot = top + img.roi_dim[1]
            # Cropping
            edit_img.image = img.image[left:right, top:bot, :]

        if verbose:
            print('Cropping completed.')

    def add_scale(self, verbose=False):
        """Add a scale to the top-right corner of the cropped image."""
        if verbose:
            print('Adding a scale bar..')

        for img in self.edited_image_list:
            scalebar = ScaleBar(img.mm_to_px)
            # Prepare a figure without axes and calculate figure sizes
            fig = plt.figure()
            ax = plt.subplot(1, 1, 1)
            plt.axis('off', frameon=False)

            # Add image and scale
            ax.imshow(img.image)
            ax.add_artist(scalebar)

            # Save the figure without borders to a temporary file
            temp_file = os.path.join(tempfile.gettempdir(), 'temp.png')
            fig.savefig(temp_file, bbox_inches='tight', pad_inches=0)
            plt.close()

            # Reload the temporary file as image object and delete it
            img.image = io.imread(temp_file)
            os.remove(temp_file)

        if verbose:
            print('Scale bar added.')

    def align(self, verbose=False):
        """
        Align images next to each other.

        If the y-axis isn't the same length, the remaining space should be
        filled with white or black space.
        """
        if verbose:
            print('Aligning images..')
        # Creating a figure
        plt.figure()

        # Adding the images to subplots
        for i, img in enumerate(self.edited_image_list):
            plt.subplot(1, self.image_count, i + 1)
            plt.axis('off', frameon=False)
            plt.imshow(img.image)

        # Filename and saving
        file_dir = os.path.dirname(os.path.realpath(__file__))
        filename = self.sample_name + '_aligned.jpg'
        filepath = os.path.join(file_dir, filename)
        plt.savefig(filepath, bbox_inches='tight', pad_inches=0, dpi=600)

        if verbose:
            print('Alignment done. Complete image saved.')


class Image(object):
    """
    Subclass of the sample class for images of each sample.

    It contains all information concerning the images, as well as
    the image-files themselves. Methods performing on a single image are
    stored here.
    """

    def __init__(self, filepath=None, image=None, load=True, verbose=False):
        """
        Instantiate an image object, load the image and set up variables.

        filepath: path of the image to be loaded (if load=True)
        image: preexisting image object (if load=False)
        load: load an image? Use False if using a preexisting one.
        """
        # Filename, Path, Name, Extension
        self.dir_name = os.path.dirname(filepath)
        self.abs_path = os.path.abspath(filepath)
        self.filename = os.path.basename(self.abs_path)
        self.name, self.extension = os.path.splitext(self.filename)

        # Image object
        if load:
            self.image = io.imread(self.abs_path)
        else:
            self.image = image

        # Magnification
        self.calculate_magnification(verbose=verbose)

        # ROI parameters
        self.roi_dim = []
        self.roi_coords = []

    def calculate_magnification(self, verbose=False):
        """Read magnification metadata and calculate the px:mm ratio."""
        mag_dir = os.path.dirname(os.path.realpath(__file__))
        mag_table = pd.read_csv(os.path.join(mag_dir, 'magnifications.csv'))
        full_px_width = 2048.

        self.px_height, self.px_width, self.channels = self.image.shape

        m = re.search(r'\d{1,2}\.?\d{1,2}x', self.name)
        try:
            self.magnification = m.group()
        except AttributeError:
            if verbose:
                print('Loading magnification failed.'
                      'Missing magnification info in filename.')
            pass

        # mm-Width
        i = mag_table.magnification == self.magnification
        self.mm_width = float(mag_table.mm_width[i])

        # Ratio
        px_ratio = self.px_width / full_px_width
        self.mm_to_px = (self.mm_width / full_px_width) * px_ratio

    def detect_roi(self, threshold=150):
        """
        Detect the square in the sample image.

        Returns ROI dimensions and coordinates.
        """
        # Find all pixels greater than threshold (arbitrary)
        img_red_thresh = self.image[:, :, 0] > threshold

        # Marching squares algorithm to find contours
        img_contours = measure.find_contours(img_red_thresh,
                                             0, fully_connected='high')

        # Find index of the biggest contour
        border = [len(x) for x in img_contours].index(max([len(x) for x in img_contours]))

        # Find the coordinates within the border
        x_points, y_points = zip(*img_contours[border])
        x_max = int(max(x_points)) - border
        y_max = int(max(y_points)) - border
        x_min = int(min(x_points)) + border
        y_min = int(min(y_points)) + border

        # The ROI dimensions
        self.roi_dim = [x_max - x_min, y_max - y_min]
        if self.roi_dim[0] == self.roi_dim[1]:
            self.is_square = True
        else:
            self.is_square = False

        # The ROI coordinates
        self.roi_coords = [x_min, y_min]
