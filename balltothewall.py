import cv2
import picamera
import picamera.array
import sys
import numpy

cascpath = sys.argv[1]
facecascade = cv2.CascadeClassifier(cascpath)
#targets = ['test1.jpg', 'test2.jpg', 'test3.jpg',
# 'test4.jpg', 'test5.jpg', 'test6.jpg']

with picamera.PiCamera() as camera:
	with picamera.array.PiRGBArray(camera) as stream:
		camera.resolution = (320, 240)
	
		while True:
			camera.color_effects = (128, 128)
			camera.capture(stream, 'bgr', use_video_port=True)
			img = stream.array
			faces = facecascade.detectMultiScale(
				img,
				minSize = (30, 30),
				scaleFactor = 1.5,
				minNeighbors = 5,
				flags = cv2.cv.CV_HAAR_SCALE_IMAGE
			)
			for(x,y,w,h) in faces:
				#cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0), 2)
				camera.capture('tar.jpg')
				#for target in targets:
				template = cv2.imread('tar.jpg',0)
				target2 = cv2.imread('test3.jpg',0)
				w, h = target2.shape[::-1]
				res = cv2.matchTemplate(template,target2,eval('cv2.TM_CCOEFF'))
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				top_left = max_loc
				bottom_right = (top_left[0] + w, top_left[1] + h)
				cv2.rectangle(template, top_left, bottom_right, 255, 0)
				cv2.imshow('frame1', template)
				cv2.imshow('frame2', target2)
					
			cv2.imshow('frame', img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			stream.seek(0)
			stream.truncate()
		cv2.destroyAllWindows()
