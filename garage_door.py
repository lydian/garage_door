# -*- coding: utf-8 -*-
import time
from signal import pause

import numpy as np
from gpiozero import DistanceSensor


ECHO_GPIO_PORT = 22
TRIGGER_GPIO_PORT = 17

class GarageDoorSensor:

    def __init__(self, echo_port, trigger_port, threshold, max_distance=4):
        self.threshold = threshold
        self.echo_port = echo_port
        self.trigger_port = trigger_port
        self.threshold = threshold
        self.max_distance = max_distance


    def get_values(self, count, time_span=0.001):
        sensor = DistanceSensor(
            echo=self.echo_port,
            trigger=self.trigger_port,
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
