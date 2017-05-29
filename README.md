# imgprep

A small script to prepare the images of my microscopy for analysis.

## Reasoning for the script

The polarization-microscope at my facility can't crop images with the standard software. Neither can it put an automatic scale into the image by itself. I will probably take 100s of images with it and don't want to crop and scale each one by hand.
Therefore I will write a small python-script for me to do it automatically. Another benefit is learning the python image processing library pillow and its basic uses.

The images will appear in triplets (normal light, polarized light, and polarized light turned by 90°). I can draw a red rectangle around objects in the microscope software.

## Script-Progress

- Initialization
  - [x] Load the all images of the same object
  - [ ] Meta-data
    - [x] Save image names and file-extensions
    - [ ] Read the magnification(x20 or x63) from the file-name
- Alteration
  - [x] Cropping
    - [x] Recognize the red square around the object
      - [ ] Recognize a square of any color
    - [x] Crop the image to the ROI
      - [ ] Crop to the insides of the square
      - [ ] Crop to squares with borders of variable width
  - [ ] Image-Arrangement
  - [ ] Scale-Bars
    - [ ] Calculate individual scale-bars for every sub-image
    - [x] Calculate positions for scale-bars
    - [x] Insert scale-bars
- Saving
  - [x] Saving the edited images
  - [ ] Save the finished arrangement of sample images into one file (.png)

---

- Testing
  - [ ] Employ basic testing structure
    - [ ] Rewrite methods to serve a single purpose
    - [ ] Write tests for every method

---

## TODO Priorities

1. Read in magnification metadata
  * Calculate scalebars
