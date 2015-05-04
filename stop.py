from grovepi import *
import math
import time

buzzer_pin = 2

pinMode(buzzer_pin, "OUTPUT")

try:
	digitalWrite(buzzer_pin, 0)

except KeyboardInterrup:
	digitalWrite(buzzer_ping, 0)

