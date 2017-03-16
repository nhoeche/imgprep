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
import matplotlib.pyplot as plt
import sample

from PIL import Image

def main():
    # Create the argparser
    parser = argparse.ArgumentParser(usage=__doc__)

    # Sample-name: Mandatory
    parser.add_argument('samplename',
                        help='The name of the sample to be treated.')

    # Load images?
    parser.add_argument('filename', nargs='+',
                        help='Filenames of images associated to the sample.')

    # Show images?
    parser.add_argument('-s', '--show', action='store_true',
                        help='Shows the imported images. Only use in con-'\
                        'junction with -i.')

    # Retain border?
    parser.add_argument('-b', '--border', action='store_true',
                        help='Retains the detection border.')

    # Verbosity?
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Add verbosity. Prints more info on the screen.')

    args = parser.parse_args()

#   ----------------------------------------------------------------------------

    # Generating a specimen
    if args.verbose:
        print('Generating a new sample named {}'.format(args.samplename))
        print('Starting the script with options {}'.format(args))
    specimen = sample.Sample(sample_name=args.samplename)
    specimen.numberofimages = len(args.filename)

    # Loading image paths
    if args.verbose:
        print('Loading the specified images.')
    specimen.image_paths = args.filename[0]
    specimen.load_images()
    if args.verbose:
        print('Detecting squares...')
    specimen.detect_square()

    # Reduces the size of the cropbox to within the colored border.
    if args.border:
        specimen.cropbox[0] -= 8
        specimen.cropbox[1] -= 8
        specimen.cropbox[2] += 8
        specimen.cropbox[3] += 8

    # Saves a copy of the cropped image
    croppedimage = specimen.image.crop(specimen.cropbox)
    croppedimage.save('{}_cropped.jpg'.format(specimen.name))

    # Showing the raw images
    if args.show:
        if args.verbose:
            print('Showing the raw images.')
        for i, image in enumerate(specimen.images):
            plt.imshow(image)
            plt.show()

if __name__ == "__main__":
    main()
