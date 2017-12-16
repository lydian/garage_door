# -*- coding: utf-8 -*-
import time
from signal import pause
from io import BytesIO
from picamera import PiCamera
import numpy as np
from gpiozero import DistanceSensor
from gpiozero.pins.rpigpio import RPiGPIOPin
import RPi.GPIO as GPIO

camera = PiCamera()
camera.led = False

class GarageDoorSensor:

    def __init__(self, echo_port, trigger_port, opener_port, light_port,
            threshold, max_distance=4):
        self.threshold = threshold
        self.echo_port = echo_port
        self.trigger_port = trigger_port
        self.opener_port = opener_port
        self.light_port = light_port
        self.threshold = threshold
        self.max_distance = max_distance


    def get_values(self, count, time_span=0.001):
        GPIO.setmode(GPIO.BCM)
        sensor = DistanceSensor(
            echo=RPiGPIOPin(self.echo_port),
            trigger=RPiGPIOPin(self.trigger_port),
            threshold_distance=self.threshold,
            max_distance=self.max_distance)
        values = np.array([
            self.get_value(sensor, time_span) for _ in range(count)])
        sensor.close()
        return values

    def get_value(self, sensor, time_span):
        time.sleep(time_span)
        return sensor.distance

    def get_trustworthy_value(self):
        values = self.get_values(1000)
        values = values[abs(values- np.mean(values)) < 3 * np.std(values)]
        return np.mean(values)

    def is_door_opened(self):
        distance = self.get_trustworthy_value()
        return distance < self.threshold

    def toggle(self, device):
        port = self.opener_port if device is 'door' else self.light_port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(port, False)
        time.sleep(0.25)
        GPIO.output(port, True)
        GPIO.cleanup()

    def capture(self):
#        return '';
        my_stream = BytesIO()
        camera.capture(my_stream, 'jpeg')
        my_stream.seek(0)
        return my_stream
