import sample

'''
This is the [imgprep] image-preparation-script. It should read in triplets of
images. Then it should recognize a red square in each, denoting the object of
interest. It can then crop to the contents of the square, put the images next
to each other and insert custom scalebars based on magnification.
'''

def main():
    specimen = sample.Sample
    # Should write a "get filenames" function for this, possibly with argparse
    specimen.filenames = ['Hofer2_63x_gekreuzt_evtl-coccolithB2.jpg',
                          'Hofer2_63x_gekreuzt_evtl-coccolithB2.jpg']
    specimen.pathes = ['sample_images', 'sample_images']

    specimen.load_images()


if __name__ == "__main__":
    main()
