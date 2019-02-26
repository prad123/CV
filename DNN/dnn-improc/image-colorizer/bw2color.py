# import necessary packages
from pyimagesearch.improc import Colorizer
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
    help="path to input black and white image")
ap.add_argument("-p", "--prototxt", type=str, required=True,
    help="path to Caffe prototxt file")
ap.add_argument("-m", "--model", type=str, required=True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--clusters", type=str, required=True,
    help="path to clusters center points")
args = vars(ap.parse_args())

# colorize the image
colorizer = Colorizer(args["prototxt"], args["model"], args["clusters"])
(orig, gray, colorized) = colorizer.predict(args["image"])

# show the images
cv2.imshow("Colorized", colorized)
cv2.imshow("Grayscale", gray)
cv2.imshow("Original", orig)
cv2.waitKey(0)
