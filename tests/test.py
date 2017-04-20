from imgprep import main
from imgprep import sample

import unittest

import numpy as np
from skimage import io


# -- imgprep.py
# -- -- Argparse
class ArgParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = main.argparser()

    def parsing(self):
        pass


# -- sample.py
# __init__ methods
class InitTest(unittest.TestCase):
    def setUp(self):
        self.sample = sample.Sample('test_sample')
        self.img = sample.Image('tests/test.png')

    def sample_init_test(self):
        self.assertEqual('test_sample', self.sample.sample_name)
        self.assertEqual(0, self.sample.image_count)
        self.assertEqual([], self.sample.image_list)
        self.assertEqual([], self.sample.cropped_images)

    def image_init_test(self):
        # Name
        self.assertEqual('tests/test.png', self.img.path)
        self.assertEqual('test', self.img.name)
        self.assertEqual('.png', self.img.extension)
        # Image-data
        np.testing.assert_array_equal(io.imread('tests/test.png'), self.img.image)
        # ROI parameters
        self.assertEqual([], self.img.box_dim)
        self.assertEqual([], self.img.box_coords)


class LoadImageTest(unittest.TestCase):
    def setUp(self):
        self.sample = sample.Sample('test_sample')

    def test_single_image(self):
        # Loading
        self.sample.load_images(['tests/test.png'])
        # Testing
        self.assertEqual(1, self.sample.image_count)
        self.assertItemsEqual(sample.Image('tests/test.png'),
                              self.sample.image_list[0])

    def test_multiple_images(self):
        # Loading
        self.sample.load_images(['tests/test.png', 'tests/test1.png'])
        # Testing
        self.assertEqual(2, self.sample.image_count)
        self.assertItemsEqual(sample.Image('tests/test.png'),
                              self.sample.image_list[0])

if __name__ == "__main__":
    unittest.main()
