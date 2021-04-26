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
        return float(hour_transformed)


    def sense(self, hour=-1):
        hour = str(hour)
        if hour == str(-1):
            ts = datetime.datetime.now()
            hour = str(ts.hour) + ':' + str(ts.minute)
        hour_transformed = self._transform_to_decimal(hour)
        values = {'hour': hour, 'hour_transformed':hour_transformed}
        for sensor in self.sensors:
            values[sensor.name] = sensor.get_value(hour=hour_transformed)
        return values

    def hacked_sense(self, hour=-1):
        hour = str(hour)
        if hour == str(-1):
            ts = datetime.datetime.now()
            hour = str(ts.hour) + ':' + str(ts.minute)

        hour_transformed = self._transform_to_decimal(hour)
        values = {'hour': hour, 'hour_transformed':hour_transformed}
        for sensor in self.sensors:
            values[sensor.name] = sensor.get_hacked_value(hour = hour_transformed)
        return values

    def get_sensors_stats(self, hour):
        hour = str(hour)
        if hour == -1:
            ts = datetime.datetime.now()
            hour = str(ts.hour) + ':' + str(ts.minute)

        hour_transformed = self._transform_to_decimal(hour)
        stats = {
            "hour" : hour_transformed,
            "sensors" : {}
        }
        for sensor in self.sensors:
            y_cent, y_min, y_max = sensor.get_sensor_stats(hour=hour_transformed)
            sensor_stats = {
                'y_cent':y_cent,
                'y_min':y_min,
                'y_max':y_max
            }
            stats['sensors'][sensor.name] = sensor_stats
        return stats

