
class Sensor:
    # abc is not supported in micropython. Sensor is an abstract class
    def pull(self):
        """Pull data from the sensor"""
       

class ESP32Temperature(Sensor):
    """for some wack reason pycom didnt decide to implement the esp32 lib"""
    def __init__(self):
        import machine
        self.machine = machine

    def pull(self) -> float:
        return ((self.machine.temperature() - 32) / 1.8)

class ESP32StackUse(Sensor):
    def __init__(self):
        import micropython
        self.mp = micropython
    
    def pull(self):
        return self.mp.stack_use()

class PyTrackGPS(Sensor):
    def __init__(self):
        from pycoproc_1 import Pycoproc
        from L76GNSS import L76GNSS
        self.py = Pycoproc(Pycoproc.PYTRACK)
        self.gps = L76GNSS(self.py, timeout=60)
        

    def pull(self) -> tuple[float, float]:
        return self.gps.coordinates()
