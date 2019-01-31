# USAGE
# python train_model.py --dataset output/data/training --features-db output/training_features.hdf5 \
#	--pbow-db output/training_pbow.hdf5 --model output/model.cpickle

# import the necessary packages
from __future__ import print_function
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
import sklearn
import numpy as np
import argparse
import pickle
import h5py
import cv2

# handle sklearn versions less than 0.18
if int((sklearn.__version__).split(".")[1]) < 18:
	from sklearn.grid_search import GridSearchCV

# otherwise, sklearn.grid_search is deprecated
# and we'll import GridSearchCV from sklearn.model_selection
else:
	from sklearn.model_selection import GridSearchCV

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="Path to the directory that contains the original images")
ap.add_argument("-f", "--features-db", required=True,
	help="Path the features database")
ap.add_argument("-p", "--pbow-db", required=True,
	help="Path to where the pyramid of bag-of-visual-words database")
ap.add_argument("-m", "--model", required=True,
	help="Path to the output classifier")
args = vars(ap.parse_args())

# open the features and bag-of-visual-words databases
featuresDB = h5py.File(args["features_db"])
bovwDB = h5py.File(args["pbow_db"])

# grab the training and testing data from the dataset using the first 300
# images as training and the remaining images for testing
print("[INFO] loading data...")
(trainData, trainLabels) = (bovwDB["bovw"][:300], featuresDB["image_ids"][:300])
(testData, testLabels) = (bovwDB["bovw"][300:], featuresDB["image_ids"][300:])

# prepare the labels by removing the filename from the image ID, leaving
# us with just the class name
trainLabels = [l.split(":")[0] for l in trainLabels]
testLabels = [l.split(":")[0] for l in testLabels]

# define the grid of parameters to explore, then start the grid search where
# we evaluate a Linear SVM for each value of C
print("[INFO] tuning hyperparameters...")
params = {"C": [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]}
model = GridSearchCV(LinearSVC(random_state=42), params, cv=3)
model.fit(trainData, trainLabels)
print("[INFO] best hyperparameters: {}".format(model.best_params_))

# show a classification report
print("[INFO] evaluating...")
predictions = model.predict(testData)
print(classification_report(testLabels, predictions))

# loop over a sample of the testing data
for i in np.random.choice(np.arange(300, 375), size=(20,), replace=False):
	# randomly grab a testing image, load it, and classify it
	(label, filename) = featuresDB["image_ids"][i].split(":")
	image = cv2.imread("{}/{}/{}".format(args["dataset"], label, filename))
	prediction = model.predict(bovwDB["bovw"][i].reshape(1, -1))[0]

	# show the prediction
	print("[PREDICTION] {}: {}".format(filename, prediction))
	cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)

# close the databases
featuresDB.close()
bovwDB.close()

# dump the classifier to file
print("[INFO] dumping classifier to file...")
f = open(args["model"], "wb")
f.write(pickle.dumps(model))
f.close()