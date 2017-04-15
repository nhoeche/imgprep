#!/usr/bin/env python3
'''
This is the "imgprep"-script for treating microscopy images.

It can read in multiple images of a sample slide [images].
Then it can also recognize a unicolor square in each, denoting the object of
interest, to crop the contents of the square. It can put the images next
to each other and insert custom scalebars based on magnification levels.

-=FILES=-
imgprep.py: Main script. Responsible for argparse and calling of the methods

sample.py:  Class for treating a sample. Contains all associated variables,
            images and methods. Get's called from imgprep.py.

THIS SCRIPT IS STILL WORK IN PROGRESS!
'''
import argparse
import os

import sample


def argparser():
    # TODO: Outsource the parser setup into it's own function
    # Create the argparser
    parser = argparse.ArgumentParser(usage=__doc__)

    # Sample-name: Mandatory
    parser.add_argument('samplename',
                        help='The name of the sample to be treated.')

    # Load images?
    parser.add_argument('filenames', nargs='+',
                        help='Filenames of images associated to the sample.')

    # Crop?
    parser.add_argument('-c', '--crop', action='store_true',
                        help='Crop images to the size of painted-in squares')

    # Verbosity?
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Add verbosity. Prints more info on the screen.')

    return parser.parse_args()


def main(args):
    # Generating a specimen
    if args.verbose:
        print('Generating a new sample named {}'.format(args.samplename))
        print('Starting the script with options {}'.format(args))

    specimen = sample.Sample(sample_name=args.samplename)
    specimen.image_count = len(args.filename)

    # Loading image paths
    if args.verbose:
        print('Loading the specified images.')

    specimen.load_images(args.filenames)

    # Cropping
    if args.crop:
        # Square detection
        if args.verbose:
            print('Starting the cropping process.')
            print('Detecting the square(s).')

        specimen.detect_square()

        # Cropping
        if args.verbose:
            print('Cropping the images.')

        specimen.crop()

    # Saving
    if args.crop:
        if args.verbose:
            print('Saving the cropped images')

            specimen.save_images()


if __name__ == "__main__":
    main(argparser())
