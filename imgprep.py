#!/usr/bin/env python3
'''
This is the [imgprep] image-preparation-script. It should read in triplets of
images. Then it should recognize a red square in each, denoting the object of
interest. It can then crop to the contents of the square, put the images next
to each other and insert custom scalebars based on magnification.
'''

import argparse
import sample


def main():
    # Create the argparser
    parser = argparse.ArgumentParser(usage=__doc__)

    # Sample info
    parser.add_argument('sample', help='The name of the sample to be treated.')

    # Image loading
    parser.add_argument('images', help='Filenames of images associated to the '\
                        'sample.')

    # Verbosity
    parser.add_argument('-v', '--verbose', help='Verbosity modus. Prints more '\
                        'info on the screen.', action='store_true')

    args = parser.parse_args()

#   ----------------------------------------------------------------------------

    # Generating a specimen
    specimen = sample.Sample(sample_name=args.sample)

    # Loading image pathes
    if args.images:
        specimen.image_pathes = [path for path in args.images]
        specimen.load_images()


if __name__ == "__main__":

    main()
