from gopigo import *
import sys
import time

led_on(LED_R)
led_on(LED_L)

for i in range(20):
	led(LED_L, 255)
	led(LED_R, 255)
	time.sleep(.25)
	led(LED_L, 0)
	led(LED_R, 0)
	time.sleep(.25)
	print i


led(LED_L, 255)
led(LED_R, 255)
time.sleep(5)
led(LED_L, 0)
led(LED_R, 0)
led_off(LED_R)
led_off(LED_L)
