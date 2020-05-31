import RPi.GPIO as GPIO
import os, time
from temperature import fetch_temp
from simple_pid import PID

TIME_STEP_SIZE = 2
RELAY_PORT = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PORT, GPIO.OUT)

def on():
    GPIO.output(RELAY_PORT, 0)

def off():
    GPIO.output(RELAY_PORT, 1)

def log(diff, measured_temp, setpoint, value=""):
    print(str(int(diff // 60)) + "m " + str(int(diff) % 60) + "s: measured(", measured_temp, ") setpoint(", setpoint, ")", value)

def get_setpoint(profile, diff):
    current_minute = diff // 60
    setpoint = 0

    for (minute, phase_temp) in profile:
            if current_minute < minute:
                setpoint = phase_temp
                break

    return setpoint

def maisch(profile, margin):
    start_time = time.time()
    while True:
        now = time.time()
        diff = now - start_time
        setpoint = get_setpoint(profile, diff)

        measured_temp = fetch_temp()

        if measured_temp + margin >= setpoint:
            off()
        elif measured_temp - margin <= setpoint:
            on()

        #print(str(int(current_minute)) + "m " + str(int(diff) % 60) + "s: measured(", measured_temp, ") setpoint(", setpoint, ")")
        log(diff, measured_temp, setpoint)

        time.sleep(TIME_STEP_SIZE)


def maisch_pid(profile, INTERVAL):
    pid = PID(10, 0, 0, setpoint=0)

    start_time = time.time()
    while True:
        now = time.time()
        diff = now - start_time
        pid.setpoint = get_setpoint(profile, diff)

        temp = fetch_temp()
        value = pid(temp)
        value = min(value, 100)
        prop = value / 100.0


        log(diff, temp, pid.setpoint, value=value)

        if value <= 0:
            off()
            time.sleep(INTERVAL)
        elif value == 100:
            on()
            time.sleep(INTERVAL)
        else:
            on()
            time.sleep(prop * INTERVAL)
            off()
            time.sleep((1 - prop) * INTERVAL)




if __name__ == '__main__':
    maischen = [
        (45, 63),
        (65, 68),
        (95, 73),
        (100, 78)
    ]

    pidtest = [(50000, 60)]

    margin = 2.5

    try:
        maisch_pid(pidtest, 10)
    except BaseException as e:
        print(e)
        off()
        exit()
