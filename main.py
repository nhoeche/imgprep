import skimage
import numpy as np

'''
This is the [imgprep] image-preparation-script. It should read in triplets of
images. Then it should recognize a red square in each, denoting the object of
interest. It can then crop to the contents of the square, put the images next
to each other and insert custom scalebars based on magnification.
'''


def main():

    filenames = ['Hofer2_63x_gekreuzt_evtl-coccolithB2.jpg',
                 'Hofer2_63x_gekreuzt_evtl-coccolithB2.jpg']
    pathes = ['sample_images', 'sample_images']

    pics = load_images(filenames, pathes)


def load_images(filenames, pathes):
    img = [i for i in range(len(filenames))]
    for i, (filename, path) in enumerate(zip(filenames, pathes)):
        img[i] = skimage.io.imread('{}/{}'.format(path, filename))
        img[i] = skimage.img_as_float(img[i])
    return img

    # TODO: Save metadata and image objects into numpy array / pandas
    #       frame
    # TODO: Rotate the second polarized image by -45°


# TODO: Recognize the Magnification and calculate scale-bar dimensions
# TODO: Recognize the Red square coordinates
# TODO: Crop the images and place them next to each other
# TODO: Create three scale-bars and insert them into the images


if __name__ == "__main__":
    main()
