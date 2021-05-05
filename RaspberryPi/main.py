from rPi import  RPi

if __name__ == '__main__':
    rpi = RPi()
    rpi.add_sensor("LIGHT_SENSOR", "lightsensor", 2)
    #rpi.add_sensor("TEMPERATURE_SENSOR", "temperaturesensor", 2)

    print(rpi.sense())



