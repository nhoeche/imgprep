#!/usr/bin/env python3
'''
This is the "imgprep"-script for treating microscopy images.

It can read in multiple images of a sample slide [images].
Then it can also recognize a unicolor square in each, denoting the object of
interest, to crop the contents of the square. It can put the images next
to each other and insert custom scalebars based on magnification levels.

By default, the full editing routine is run. Use command line arguments like
-c -s to skip certain steps.

THIS SCRIPT IS STILL WORK IN PROGRESS!
'''
import argparse


def argparser():
    """Create the argparser."""
    parser = argparse.ArgumentParser(usage=__doc__)

    # Sample-name: Mandatory
    parser.add_argument('samplename',
                        help='The name of the sample to be treated.')
    # Load images?
    parser.add_argument('filenames', nargs='+',
                        help='Filenames of images associated to the sample.')
    # Crop?
    parser.add_argument('-c', '--no-crop', action='store_false',
                        default=True, dest='crop',
                        help='Do not crop the images.')
    # Scalebar?
    parser.add_argument('-s', '--no-scale', action='store_false',
                        default=True, dest='scale',
                        help='Do not add a scalebar to the images.')
    # Align?
    parser.add_argument('-a', '--no-align', action='store_false',
                        default=True, dest='align',
                        help='Do not add a align the images.')
    # Verbosity?
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Add verbosity. Prints more info on the screen.')
    return parser.parse_args()


def main(args):
    """Execute the program"""
    # Generating a specimen
    specimen = sample.Sample(args.samplename, verbose=args.verbose)

    # Loading images
    specimen.load_images(args.filenames, verbose=args.verbose)
    specimen.init_editing()

    # Cropping
    if args.crop:
        specimen.crop(verbose=args.verbose)

    # Scale Bar
    if args.scale:
        specimen.add_scale(verbose=args.verbose)

    if args.align:
        specimen.align(verbose=args.verbose)

    # Saving
    if args.crop or args.scale:
        specimen.save_images(verbose=args.verbose)


if __name__ == "__main__":
    import sample
    main(argparser())
