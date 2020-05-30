import os, time

devices = [
    "28-0316a645fdff"
]

def fetch_temp():
    for dev in devices:
        command = "cat /sys/bus/w1/devices/" + dev + "/w1_slave 2> /dev/null | grep \"t=[0-9]*\" -o | grep [0-9]* -o"
        temp = os.popen(command).read()

        temperature = 0
        try:
            temperature = int(temp)
        except ValueError as e:
            pass

        return temperature / 1000.0


if __name__ == '__main__':
    while True:
        print(fetch_temp())
        time.sleep(1)
