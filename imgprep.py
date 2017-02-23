#!/usr/bin/env python3

'''
This is the "imgprep"-script for treating microscopy images.

It can read in multiple images of a sample slide [images].
Then it can also recognize a unicolor square in each, denoting the object of
interest, to crop the contents of the square. It can put the images next
to each other and insert custom scalebars based on magnification levels.

THIS SCRIPT IS STILL WORK IN PROGRESS!
'''

import argparse

import sample


def main():
    # Create the argparser
    parser = argparse.ArgumentParser(usage=__doc__)

    # Sample info
    parser.add_argument('sample',
                        help='The name of the sample to be treated.')

    # Image loading
    parser.add_argument('-i', '--images', nargs='+',
                        help='Filenames of images associated to the sample.')

    # Verbosity
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Add verbosity. Prints more info on the screen.')

    args = parser.parse_args()

#   ----------------------------------------------------------------------------

    # Generating a specimen
    specimen = sample.Sample(sample_name=args.sample)

    # Loading image pathes
    if args.images:
        specimen.image_pathes = args.images
        specimen.load_images()


if __name__ == "__main__":

    main()
