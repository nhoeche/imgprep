import skimage
import skimage.io


class Sample(object):
    '''
    The sampe class for the imgprep script. One object of this class contains
    three images of the sample. It also defines the methods used to process
    the images.
    '''

    def __init__(self, sample_name):
        '''
        Creates instances of the Sample class.
        '''

        self.name = sample_name

        self.image_pathes = []
        self.images = []

    def load_images(self):
        '''
        Loads microscope images of the sample as numpy arrays and saves the
        image metadata. Make sure to have filenames and image_pathes set so
        load the images.
        '''
        self.images = [None] * len(self.image_pathes)

        for i, path in enumerate(self.image_pathes):
            self.images[i] = skimage.io.imread(path)
            self.images[i] = skimage.img_as_float(self.images[i])

        # TODO: Save metadata
        # TODO: Maybe rotate the second polarized image by -45°

    def square_detect(image):
        '''
        Detect a drawn square in the microscope images for later cropping.
        '''
        # Copypasted, functionality not guaranteed
        # cols = (image[..., 0] == 255).sum(0)
        # left = cols.argsort()[-2:].min()
        # right = cols.argsort()[-2:].max()
        pass

    # TODO: Recognize the Magnification and calculate scale-bar dimensions
    # TODO: Recognize the Red square coordinates
    # TODO: Crop the images and place them next to each other
    # TODO: Create three scale-bars and insert them into the images
