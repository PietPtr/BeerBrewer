import RPi.GPIO as GPIO
import os, time
from temperature import fetch_temp

TIME_STEP_SIZE = 2
RELAY_PORT = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PORT, GPIO.OUT)

def on():
    GPIO.output(RELAY_PORT, 0)

def off():
    GPIO.output(RELAY_PORT, 1)

def maisch(profile, margin):
    start_time = time.time()
    while True:
        now = time.time()
        diff = now - start_time
        current_minute = diff // 60
        setpoint = 0

        for (minute, phase_temp) in profile:
            if current_minute < minute:
                setpoint = phase_temp
                break

        measured_temp = fetch_temp()

        if measured_temp + margin >= setpoint:
            off()
        elif measured_temp - margin <= setpoint:
            on()

        print(str(int(current_minute)) + "m " + str(int(diff) % 60) + "s: measured(", measured_temp, ") setpoint(", setpoint, ")")

        time.sleep(TIME_STEP_SIZE)


if __name__ == '__main__':
    profiel = [
        (5, 58),
        (50, 62),
        (53, 68),
        (60, 72)
    ]

    margin = 2.5

    try:
        maisch(profiel, margin)
    except BaseException as e:
        print(e)
        off()
        exit()
