# imgprep

A small script to prepare the images of my microscopy for analysis.

## Reasoning for the script

Many microscopy softwares can't crop images with the standard software. Neither can they put an automatic scale into the image by itself. When processing a huge amount of images, it can be tedious to edit every image by hand.
Tis small python-script tries to do that automatically. Another benefit is learning the python image processing libraries their basic uses.

The script always treats one sample at a time. Multiple images can be associated to one sample. Draw red squares around your images beforehand. The software will recognize the square and crop the image to it.
Also provide a csv file providing the magnification data (e.g. 63x magnification = 0.135mm screen width). The program will read it and use it to automatically add a scale to your images.

Please report any bugs / concerns / improvements.

## Script-Progress

- Initialization
  - [x] Load the all images of the same object
  - [x] Meta-data
    - [x] Read image names and file-extensions
    - [x] Read the magnification(x20 or x63) from the file-name
- Alteration
  - [x] Cropping
    - [x] Recognize the red square around the object
      - [ ] Recognize a square of any color
    - [x] Crop the image to the ROI
      - [ ] Crop to the insides of the square
      - [ ] Crop to squares with borders of variable width
  - [x] Image-Arrangement
  - [x] Scale-Bars
    - [x] Calculate individual scale-bars for every sub-image
    - [x] Calculate positions for scale-bars
    - [x] Insert scale-bars
- Saving
  - [x] Saving the edited images
  - [x] Save the finished arrangement of sample images into one file (.png)

## TODO Priorities

1. Revise code to shorten it and make it more intuitive
  * Rewrite saving methods (export saving from alignment method into regular saving)
2. Remove white borders from matplotlib figures (`add_scale` and `align` methods)
3. Change all hard-coding to be more flexible
  * Magnification table
  * Red square -> any square