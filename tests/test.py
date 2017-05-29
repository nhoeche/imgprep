"""Tests for the imgprep project."""
from imgprep import main
from imgprep import sample

import unittest
import os
import numpy as np
from skimage import io


# -- imgprep.py
# -- -- Argparse
class ArgParserTest(unittest.TestCase):
    """Test the argparser in main.py."""

    def setUp(self):
        self.parser = main.argparser()

    def parsing(self):
        pass


# -- sample.py
# __init__ methods
class InitTest(unittest.TestCase):
    def setUp(self):
        self.sample = sample.Sample('test_sample')
        self.img = sample.Image('tests/test_63x.png')

    def sample_init_test(self):
        self.assertEqual('test_sample', self.sample.sample_name)
        self.assertEqual(0, self.sample.image_count)
        self.assertEqual([], self.sample.image_list)
        self.assertEqual([], self.sample.edited_images)

    def image_init_test(self):
        # Name
        self.assertEqual('/home/nils/Documents/Programming/Py/imgprep/tests/test_63x.png', self.img.abs_path)
        self.assertEqual('tests', self.img.dir_name)
        self.assertEqual('test_63x.png', self.img.filename)
        self.assertEqual('test_63x', self.img.name)
        self.assertEqual('.png', self.img.extension)
        # Image-data
        np.testing.assert_array_equal(io.imread('tests/test_63x.png'),
                                      self.img.image)
        # ROI parameters
        self.assertEqual([], self.img.box_dim)
        self.assertEqual([], self.img.box_coords)


class LoadImageTest(unittest.TestCase):
    def setUp(self):
        self.sample = sample.Sample('test_sample')

    def test_single_image(self):
        # Loading
        self.sample.load_images(['tests/test_63x.png'])
        # Testing
        self.assertIsNotNone(self.sample.image_list[0])
        self.assertEqual(1, self.sample.image_count)
        self.assertIsInstance(self.sample.image_list[0], sample.Image)

    def test_multiple_images(self):
        # Loading
        self.sample.load_images(['tests/test_63x.png', 'tests/test1_63x.png'])
        # Testing
        self.assertEqual(2, self.sample.image_count)

        self.assertIsNotNone((self.sample.image_list[0],
                              self.sample.image_list[1]))
        self.assertIsNot(self.sample.image_list[0],
                         self.sample.image_list[1])
        self.assertIsInstance(self.sample.image_list[0], sample.Image)
        self.assertIsInstance(self.sample.image_list[1], sample.Image)


class SaveImageTest(unittest.TestCase):
    def setUp(self):
        self.cwd = 'tests'
        self.file1 = os.path.join(self.cwd, 'test_63x.png')
        self.file2 = os.path.join(self.cwd, 'test1_63x.png')
        self.sample = sample.Sample('test_sample')

    def tearDown(self):
        if os.path.isfile(os.path.join(self.cwd, 'test_63x_edited.png')):
            os.remove(os.path.join(self.cwd, 'test_63x_edited.png'))
        if os.path.isfile(os.path.join(self.cwd, 'test1_63x_edited.png')):
            os.remove(os.path.join(self.cwd, 'test1_63x_edited.png'))

    def test_single_image(self):
        # Loading
        self.sample.load_images([self.file1])
        self.sample.crop()
        self.sample.save_images()
        # Filename
        filename = os.path.join(self.cwd, 'test_63x_edited.png')
        # Checking if file exists
        self.assertTrue(os.path.isfile(filename))

    def test_multiple_images(self):
        # Loading
        self.sample.load_images([self.file1, self.file2])
        self.sample.crop()
        self.sample.save_images()
        # Filename
        filename = os.path.join(self.cwd, 'test_63x_edited.png')
        filename1 = os.path.join(self.cwd, 'test1_63x_edited.png')
        # Checking if file exists
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.path.isfile(filename1))


class ROIDetectTest(unittest.TestCase):
    def setUp(self):
        self.img = sample.Image('tests/test_63x.png')
        self.img.detect_roi()

    def test_x_coord(self):
        self.assertAlmostEqual(self.img.roi_coords[0], 141, delta=5)

    def test_y_coord(self):
        self.assertAlmostEqual(self.img.roi_coords[1], 241, delta=5)

    def test_x_dim(self):
        self.assertAlmostEqual(self.img.roi_dim[0], 145, delta=20)

    def test_y_dim(self):
        self.assertAlmostEqual(self.img.roi_dim[1], 130, delta=20)


class ScaleTest(unittest.TestCase):
    """Class for testing calculation and integration of the scale bar."""

    def setUp(self):
        self.img = sample.Image('tests/test_63x.png')
        pass

    def test_ratio_calculation(self):
        """Test whether the ratio for the scale is calculated correctly."""
        self.assertEqual(self.img.px_width, self.img.image.shape[1])
        self.assertEqual(self.img.mm_width, 0.135)
        self.assertAlmostEqual(self.img.mm_to_px, 0.000020953, places=8)
        pass

if __name__ == "__main__":
    loader = unittest.TestLoader()
    # Load tests into suite
    suite = loader.loadTestsFromTestCase((InitTest,
                                          LoadImageTest,
                                          SaveImageTest,
                                          ROIDetectTest))
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)
