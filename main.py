from PIL import Image


def main():

    filenames = []
    pathes = []
    load_images(filenames, pathes)

def load_images(filenames, pathes):

    img = list(length(filenames))

    for i, (filename, path) in enumerate(zip(filenames, pathes)):
        img[i] = Image.open('{}/{}'.format(filename, path))


if __name__ == "__main__":
    main()
