import json
from abc import abstractmethod
from distributionGenerator import DistributionGenerator
import os
import numpy as np

class SensorsTypes:
    def __init__(self):
        self.LIGHT_SENSOR = "LIGHT_SENSOR"
        self.TEMPERATURE_SENSOR = "TEMPERATURE_SENSOR"

class Sensor():
    def __init__(self, name, tolerance):
        self.name = name
        self.tolerance = tolerance
        self.d_values = self.get_distribution_values(self.name)
        self.distribution = DistributionGenerator(y = self.d_values, tolerance = tolerance)

    def get_distribution_values(self,name):
        name += '.json'
        path = os.path.join(os.getcwd(), 'distributions', name)
        try:
            with open(path, 'r') as fp:
                values = json.load(fp)
        except FileNotFoundError as e:
            print(e)

        return values

    def get_sensor_stats(self, hour):
        return self.distribution.evaluate(x = hour)

    def get_value(self, hour):
        if hour >= 0.0 and hour <= 23.59:
            _, y_min, y_max = self.distribution.evaluate(x=hour)
            return np.round(np.random.uniform(low=y_min, high = y_max),2)
        else:
            print("Hour not valid")
            return -88.88888

    def get_hacked_value(self, hour):
        if hour >= 0.0 and hour <= 23.59:
            _, y_min, y_max = self.distribution.evaluate(x=hour)
            upper_hacked_value = np.round(np.random.uniform(low=y_max + 0.1, high=y_max + self.tolerance),2)
            lower_hacked_value = np.round(np.random.uniform(low=y_min - self.tolerance, high=y_min - 0.1),2)
            ret = upper_hacked_value if np.random.rand() > 0.5 else lower_hacked_value
            return ret
        else:
            print("Hour not valid")
            return -88.88888




class LightSensor(Sensor):
    def __init__(self, name, tolerance):
        super(LightSensor,self).__init__(name, tolerance)


class TemperatureSensor(Sensor):
    def __init__(self, name, tolerance):
        super(TemperatureSensor, self).__init__(name, tolerance)


if __name__ == "__main__":
    lightSensor = LightSensor('lightsensor', 2)
    print(lightSensor.get_value(hour = 12.5))