# imgprep

A small script to prepare the images of my microscopy for analysis.

## Reasoning for the script

The polarization-microscope at my facility can't crop images with the standard software. Neither can it put an automatic scale into the image by itself. I will probably take 100s of images with it and don't want to crop and scale each one by hand.
Therefore I will write a small python-script for me to do it automatically. Another benefit is learning the python image processing library pillow and its basic uses.

The images will appear in triplets (normal light, polarized light, and polarized light turned by 90°). I can draw a red rectangle around objects in the microscope sowftware.

## Script-Layout and Progress

1. [ ] Load the three images of the same object
2. [ ] Read the magnification(x20 or x63) from the filename
3. [ ] Read the absolute scale (in mm) from a magnification table .txt

4. [ ] Recognize the red rquare around the object
5. [ ] Crop the image to the insides of the red square
6. [ ] Put the three cropped images side by side
7. [ ] generate an individual scalebar for all three sub-images

-> Profit
