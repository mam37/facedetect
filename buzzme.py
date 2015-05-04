from grovepi import *
import math
import time

buzzer_pin = 2

pinMode(buzzer_pin, "OUTPUT")

def buzzme():
	try:
		digitalWrite(buzzer_pin, 1)
		time.sleep(0.25)
		digitalWrite(buzzer_pin, 0)
		time.sleep(0.25)

	except KeyboardInterrupt:
		digitalWrite(buzzer_pin, 0)

buzzme()
buzzme()
