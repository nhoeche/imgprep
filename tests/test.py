from imgprep import main
from imgprep import sample

import unittest
import os
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
        np.testing.assert_array_equal(io.imread('tests/test.png'),
                                      self.img.image)
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
        self.assertIsNotNone(self.sample.image_list[0])
        self.assertEqual(1, self.sample.image_count)
        self.assertIsInstance(self.sample.image_list[0], sample.Image)

    def test_multiple_images(self):
        # Loading
        self.sample.load_images(['tests/test.png', 'tests/test1.png'])
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
        self.file1 = os.path.join(self.cwd, 'test.png')
        self.file2 = os.path.join(self.cwd, 'test1.png')
        self.sample = sample.Sample('test_sample')

    def tearDown(self):
        os.remove(os.path.join(self.cwd, 'test_cropped.png'))
        os.remove(os.path.join(self.cwd, 'test1_cropped.png'))

    # def test_uncropped(self):
    #     self.sample.load_images(['test.png'])
        # self.assertRaises(self.sample.save_image)

    def test_single_image(self):
        # Loading
        self.sample.load_images(self.file1)
        self.sample.crop()
        self.sample.save_images(cropped=True)
        # Filename
        filename = os.path.join(self.cwd, 'test_cropped.png')
        # Checking if file exists
        self.assertTrue(os.path.isfile(filename))

    def test_multiple_images(self):
        # Loading
        self.sample.load_images((self.file1, self.file2))
        self.sample.crop()
        self.sample.save_images(cropped=True)
        # Filename
        filename = os.path.join(self.cwd, 'test_cropped.png')
        filename1 = os.path.join(self.cwd, 'test1_cropped.png')
        # Checking if file exists
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.path.isfile(filename1))


class ROIDetectTest(unittest.TestCase):
    def setUp(self):
        self.img = sample.Image('tests/test.png')
        self.img.detect_roi()

    def test_x_coord(self):
        self.assertAlmostEqual(self.img.roi_coords[0], 141, delta=5)

    def test_y_coord(self):
        self.assertAlmostEqual(self.img.roi_coords[1], 241, delta=5)

    def test_x_dim(self):
        self.assertAlmostEqual(self.img.roi_dim[0], 145, delta=20)

    def test_y_dim(self):
        self.assertAlmostEqual(self.img.roi_dim[1], 130, delta=20)


if __name__ == "__main__":
    loader = unittest.TestLoader()
    # Load tests into suite
    suite = loader.loadTestsFromTestCase((InitTest,
                                          LoadImageTest,
                                          SaveImageTest,
                                          ROIDetectTest))
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)
