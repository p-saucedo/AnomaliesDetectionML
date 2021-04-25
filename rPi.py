from sensors import LightSensor, TemperatureSensor, SensorsTypes
import numpy as np
import datetime

stypes = SensorsTypes()

class RPi:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor_type, name, tolerance):
        if sensor_type == stypes.LIGHT_SENSOR:
            sensor = LightSensor(name = name, tolerance = tolerance)
            self.sensors.append(sensor)
        elif sensor_type == stypes.TEMPERATURE_SENSOR:
            sensor = TemperatureSensor(name=name, tolerance=tolerance)
            self.sensors.append(sensor)
        else:
            print("Sensor type unknown")

    def get_sensors(self):
        return self.sensors

    def _transform_to_decimal(self, hour):
        minutes = hour.split(':')[1]
        hour = hour.split(':')[0]
        minutes_transformed = int(np.round((50 * int(minutes)) / 30,0))
        hour_transformed = hour + '.' + str(minutes_transformed)
        return np.round(float(hour_transformed),2)


    def sense(self, hour=-1):
        if hour == -1:
            ts = datetime.datetime.now()
            hour = str(ts.hour) + ':' + str(ts.minute)

        hour_transformed = self._transform_to_decimal(hour)
        values = {'hour' : hour_transformed}
        for sensor in self.sensors:
            values[sensor.name] = sensor.get_value(hour = hour_transformed)
        return values

