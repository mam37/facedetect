from gopigo import *
import cv2
import picamera
import picamera.array
import sys
import eigenface
import atexit
atexit.register(stop)

MIKE = 42
JOSH = 41

def led_blink(s):
	time_mult = 2
	time_pause = 0.25
	led_on(LED_R)
	led_on(LED_L)
	for i in range(s*time_mult):
		led(LED_L, 255)
		led(LED_R, 255)
		time.sleep(time_pause)
		led(LED_L, 0)
		led(LED_R, 0)
		time.sleep(time_pause)
	led_off(LED_R)
	led_off(LED_L)

def led_pause(s):
	led_on(LED_R)
	led_on(LED_L)
	led(LED_L, 255)
	led(LED_R, 255)
	time.sleep(s)
	led(LED_L, 0)
	led(LED_R, 0)
	led_off(LED_R)
	led_off(LED_L)

# train for face detection
cascpath = 'haarcascade_frontalface_alt.xml' 
facecascade = cv2.CascadeClassifier(cascpath)

# train for face recognition
recognizer = eigenface.face_id()


print "\nTraining complete\n"

#set_speed(100)
#right_rot()

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
				# draw green rectangle around face detected
				#cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0), 2)
				# crop image
				crop_img = img[y:y+h, x:x+w]
				# resize image
				resized = cv2.resize(crop_img, (92, 112), interpolation=cv2.INTER_AREA)
				# convert image to grayscale
				#resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
				# equalize histogram
				#resized = cv2.equalizeHist(resized)
				cv2.imwrite("test_faces/test.pgm", resized) 
				#cv2.imshow("test_faces.pgm", resized) 
				#cv2.waitKey(0)
				face, dist = recognizer.identify()
				print "Face: " + str(face) + ", distance " + str(dist)
				if face == MIKE:
					led_blink(5) 
				elif face == JOSH:
					led_pause(5)

			#cv2.imshow('frame', img)
			#if cv2.waitKey(1) & 0xFF == ord('q'):
			#	break
			stream.seek(0)
			stream.truncate()
		#cv2.destroyAllWindows()
