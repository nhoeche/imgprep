'''
Function to search for a unicolor bounding box
and return it as a cropped image.
'''

from PIL import Image

def cropimage(filename):
    im = Image.open(filename)
    px = im.load()

    xlist = []
    ylist = []
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            # Looks for R>236 G<40 color values and stores them in a list.
            if px[x,y][0] > 239 and px[x,y][1] < 40:
                xlist.append(x)
                ylist.append(y)

    # Corners of the bounding box
    xl = min(xlist) # Left
    xr = max(xlist) # Right
    yt = min(ylist) # Top
    yb = max(ylist) # Bottom
    cropbox = (xl, yt, xr, yb)
    print('Returned cropped image')
    return im.crop(cropbox)

