# import necessary packages
from imutils import paths
import progressbar
import cv2
import os

class SimpleDatasetRenamer:
  def __init__(self, path, prefix="IMG-", suffix=None, move=False, remove=False):
    # store the prefix and the paths
    self.prefix = prefix
    self.path = path
    
  def rename(self):
    # grab the reference to the list of images
    imagePaths = list(paths.list_images(self.path))
    
    # initialize the progressbar (feedback to user on the task progress)
    widgets = ["Renaming Dataset: ", progressbar.Percentage(), " ",
      progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(imagePaths),
      widgets=widgets).start()
    
    # loop over each image, then rename it and save it in its
    # original data format
    for (i, path) in enumerate(imagePaths):
      # grab the original image and the data format 
      # to encode the file with the same after renaming
      image = cv2.imread(path)
      original = path.split(os.path.sep)[-1]
      dataFormat = original.split(".")[1]
      
      # create a *unique* ID for this image relative to other processed images
      # *at the same time*
      idx = str(i).zfill(9)
      
      # initialize our filename as an empty string
      filename = ""
      
      # construct the filename based on prefix, idx, suffix and dataformat  
      filename += str(prefix) if prefix is not None else ""
      filename += idx
      filename += str(suffix) if suffix is not None else ""
      filename += dataFormat
      
      # write image to disk in the approriate directory
      print("[INFO] rename: {} \t to: {}".format(original, dataFormat))
      if move:
        cv2.imwrite(filename, image)
      else:
        directory = os.path.dirname(path)
        filename = directory + filename
        cv2.imwrite(filename, image)
      
      # check to see if we need to remove the old file      
      if remove:
        os.remove(path)
    
      # update the progressbar (feedback to user)
      pbar.update()
    
    # close the progressbar
    pbar.finish()
