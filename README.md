# imgprep

A small script to prepare the images of my microscopy for analysis.

## Reasoning for the script

The polarization-microscope at my facility can't crop images with the standard software. Neither can it put an automatic scale into the image by itself. I will probably take 100s of images with it and don't want to crop and scale each one by hand.
Therefore I will write a small python-script for me to do it automatically. Another benefit is learning the python image processing library pillow and its basic uses.

The images will appear in triplets (normal light, polarized light, and polarized light turned by 90°). I can draw a red rectangle around objects in the microscope software.

## Script-Structure and Progress

- Initialization
  - [x] Load the three images of the same object
  - [ ] Meta-data
    - [ ] Read the magnification(x20 or x63) from the file-name
    - [ ] Read the absolute scale (in mm) from a magnification table .txt
- Alteration
  - [ ] Cropping
    - [ ] Recognize the red square around the object
    - [ ] Crop the image to the insides of the red square
  - [ ] Image-Arrangement
  - [ ] Scale-Bars
    - [ ] Calculate individual scale-bars for every sub-image
    - [ ] Calculate positions for scale-bars
    - [ ] Insert scale-bars

-> Profit
