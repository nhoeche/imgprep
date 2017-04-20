from imgprep import main
from imgprep import sample

import unittest

import numpy as np
from skimage import io


# -- imgprep.py
# -- -- Argparse
class ArgParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_verbosity(self):
        pass


# -- sample.py
# -- -- Sample
class SampleTest(unittest.TestCase):
    def setUp(self):
        pass

    # -- -- image Loading
    def test_loading(self):
        pass


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
