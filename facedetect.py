import cv2
import picamera
import picamera.array
import sys

cascpath = sys.argv[1]
facecascade = cv2.CascadeClassifier(cascpath)

with picamera.PiCamera() as camera:
	with picamera.array.PiRGBArray(camera) as stream:
		camera.resolution = (320, 240)
	
		while True:
			#camera.color_effects = (128, 128)
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
				cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0), 2)



			cv2.imshow('frame', img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			stream.seek(0)
			stream.truncate()
		cv2.destroyAllWindows()
