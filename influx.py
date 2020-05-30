import os
import time
from temperature import fetch_temp
from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin')
client.switch_database('temps')

def log_temp(temperature):
    t = int(time.time())

    print(str(t) + ": "+ str(temperature) + " degrees")

    log_time = datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ')

    json_body = [{
        'measurement': 'temperature',
        'time': log_time,
        'fields': { 'temperature': temperature }
    }]

    client.write_points(json_body)


if __name__ == '__main__':
    while True:
        time.sleep(1)
        temperature = fetch_temp()
        log_temp(temperature)
