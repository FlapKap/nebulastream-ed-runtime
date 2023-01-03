# main.py -- put your code here!
import json
import io
import logging
from sensors import Sensors
from connection import LoRaWAN

import protocol
import environment
import micropython
from unittest import unittest
import tests

# set compilation optimization level
micropython.opt_level(0) # no optimization. __debug__ = True

if __debug__:
    unittest.main(tests)
    import sys
    sys.exit()

# load config
config = json.load(io.open("config.json", mode='r'))
lora_config = config["lora"]

# set up logging
loglevel = {"info": logging.INFO, "warning": logging.WARNING,
            "debug": logging.DEBUG, "error": logging.ERROR}[config["loglevel"]]
logging.basicConfig(level=loglevel, force=True)
logger = logging.getLogger(__name__)

logger.info("config loaded")
logger.info("loglevel set to {}".format(loglevel))

## set up sensors
logger.info("initialising sensors...")
sensors = Sensors(config["sensors"])
logger.info("{} sensors initialized".format(sensors.sensor_count()))

# set up pipe
## so far each operation has its own stack
## set up environment with first pull of sensor data
readings = [s.pull() for s in sensors]
environment.replace_environment(readings)
logger.debug("environment initialized with first sensor pull: {}".format(readings))

# # set up connection

logger.info("initialising connection")
lora = LoRaWAN(lora_config["joineui"], lora_config["appkey"])
lora.connect()
logger.info("waiting for incoming configuration...")
msg = lora.recieve_blocking()
operations = protocol.decode_input_msg(msg)
logger.info("configuration recieved: {} operators".format(len(operations)))


for op in operations:
    logger.debug("oper: {}".format(op))
    op()



logging.shutdown()


# calc = Calculator(bytes([CONST, 2, CONST, 3, ADD, CONST, 5, LT]))
# print(calc.execute())

# logging.shutdown()