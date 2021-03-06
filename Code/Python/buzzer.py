#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

mapping = { 11: "red", 12: "blue", 13: "green", 16: "yellow" }
lastStamp = 0

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)


def buzzer_pressed(channel):
    global lastStamp

    if time.time() - lastStamp < 5:
        print('Ignore button press %d' % mapping[channel])
        return

    url = "/api/insertBuzzer/%d" % mapping[channel]
    lastStamp = time.time()

    try:
        with open("buzzed", "w") as f:
            f.write(mapping[channel])
    except:
        print('Request failed')


for pin in mapping.keys():
    GPIO.setup(pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=buzzer_pressed)

try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    GPIO.cleanup()
