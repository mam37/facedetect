from sklearn.decomposition import RandomizedPCA
import numpy as np
import glob
import cv2
import math
import os.path
import string

IMG_RES = 92 * 112 # img resolution
NUM_EIGENFACES = 10 # images per train person
NUM_TRAINIMAGES = 400 # total images in training set

class face_id:

	def __init__(self):
		#loading training set from folder train_faces
		folders = glob.glob('train_faces/*')
		
		# Create an array with flattened images X
		# and an array with ID of the people on each image y
		X = np.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8')
		self.y = []

		# Populate training array with flattened imags from 
		# subfolders of train_faces and names
		c = 0
		for x, folder in enumerate(folders):
			train_faces = glob.glob(folder + '/*')
			for i, face in enumerate(train_faces):
				X[c,:] = self.prepare_image(face)
				self.y.append(self.ID_from_filename(face))
				c = c + 1

		# perform principal component analysis on the images
		self.pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
		self.X_pca = self.pca.transform(X)

	#function to get ID from filename
	def ID_from_filename(self, filename):
		part = string.split(filename, '/')
		return part[1].replace("s", "")

	#function to convert image to right format
	def prepare_image(self, filename):
		img_color = cv2.imread(filename)
		img_gray = cv2.cvtColor(img_color, cv2.cv.CV_RGB2GRAY)
		img_gray = cv2.equalizeHist(img_gray)
		return img_gray.flat

	def identify(self):
		# load test faces (usually one), located in folder test_faces
		test_faces = glob.glob('test_faces/*')

		# Create an array with flattened images X
		X = np.zeros([len(test_faces), IMG_RES], dtype='int8')

		# Populate test array with flattened imags from subfolders of train_faces 
		for i, face in enumerate(test_faces):
			X[i,:] = self.prepare_image(face)

		# run through test images (usually one)
		for j, ref_pca in enumerate((self.pca).transform(X)):
			distances = []
			# Calculate euclidian distance from test image to each of the known images and save distances
			for i, test_pca in enumerate(self.X_pca):
				dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
				distances.append((dist, self.y[i]))

			found_ID = min(distances)[1]
			#print "Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])  + ")"
			return found_ID, min(distances)[0]
