

class Sensor:
    # abc is not supported in micropython. Sensor is an abstract class
    def pull(self):
        """Pull data from the sensor"""


class ESP32Temperature(Sensor):
    """for some wack reason pycom didnt decide to implement the esp32 lib"""

    def __init__(self):
        import machine
        self.machine = machine

    def pull(self) -> int:
        return int((self.machine.temperature() - 32) / 1.8)


class ESP32StackUse(Sensor):
    def __init__(self):
        import micropython
        self.mp = micropython

    def pull(self) -> int:
        return self.mp.stack_use()


class PyTrackGPS(Sensor):
    def __init__(self):
        from pycoproc_1 import Pycoproc
        from L76GNSS import L76GNSS
        self.py = Pycoproc(Pycoproc.PYTRACK)
        self.gps = L76GNSS(self.py, timeout=60)

    def pull(self) -> tuple[float, float]:
        return self.gps.coordinates()


class Sensors:
    """
    Class to handle sensors. Should only be initialised once
    When initialised with a config, which is a list of the names of sensors to start,
    then it can be called

    possible improvement: rewrite to fully emulate list
    """
    def __init__(self, config: list[str]):
        sensors = []
        indexmap = {}
        for i, sens in enumerate(config):
            indexmap[sens] = i
            if sens == "ESP32Temperature":
                sensors.append(ESP32Temperature())
            elif sens == "ESP32StackUse":
                sensors.append(ESP32StackUse())

        self.__sensors = sensors
        self.__sensorindex = indexmap

    def __iter__(self):
        return iter(self.__sensors)

    def __len__(self):
        return len(self.__sensors)

    def __get_item__(self, i):
        return self.readSensor(i)

    def readSensor(self, e):
        if isinstance(e, int):
            return self.__sensors[e].pull()
        if isinstance(e, str):
            return self.__sensors[self.__sensorindex[e]].pull()

    def sensor_count(self):
        return len(self.__sensors)

