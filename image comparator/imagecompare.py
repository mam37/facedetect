from skimage.measure import structural_similarity as ssim
import cv2

def image_compare(imagea, imageb):
	s = ssim(imagea, imageb)
	cv2.imshow('orig', imagea)
	cv2.imshow('test', imageb)
	print("ssim= ", s)

original = cv2.imread("test.jpg")
test = cv2.imread("test1.jpg")

original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
test = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

image_compare(original, test)
