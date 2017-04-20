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
# -- -- Sample
class SampleTest(unittest.TestCase):
    def setUp(self):
        self.sample = sample.Sample('test_sample')

    def test_init(self):
        self.assertEqual('test_sample', self.sample.sample_name)
        self.assertEqual([], self.sample.image_list)
        self.assertEqual(0, self.sample.image_count)
        self.assertEqual([], self.sample.cropped_images)

    def test_loading(self):
        self.sample.load_images(['tests/test.png'])

        self.assertEqual(1, self.sample.image_count)

        self.assertItemsEqual(sample.Image('tests/test.png'),
                              self.sample.image_list[0])


# -- -- Image
class ImageTest(unittest.TestCase):
    def setUp(self):
        self.img = sample.Image('tests/test.png')

    def test_init(self):
        # Name
        self.assertEqual('tests/test.png', self.img.path)
        self.assertEqual('test', self.img.name)
        self.assertEqual('.png', self.img.extension)
        # Image
        np.testing.assert_array_equal(io.imread('tests/test.png'), self.img.image)
        # ROI parameters
        self.assertEqual([], self.img.box_dim)
        self.assertEqual([], self.img.box_coords)


if __name__ == "__main__":
    unittest.main()
