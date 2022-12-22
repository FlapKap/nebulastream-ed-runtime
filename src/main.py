# main.py -- put your code here!
import socket
import json
import io
import logging
import time
from sensors import ESP32Temperature, PyTrackGPS
from connection import LoRaWAN
from expression import *
from operators import *
import micropython



# set compilation optimization level
micropython.opt_level(0) # no optimization. __debug__ = True

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

# set up pipe
operations = []
value = None

for op in operations:
    logger.debug("oper: {}, val: {}".format(op,value))
    value = op(value)
    if value is None:
        break


print(value)
logging.shutdown()
# # set up connection

# logger.info("initialising connection")
# lora = LoRaWAN(lora_config["joineui"], lora_config["appkey"])
# logger.debug("hej")

# calc = Calculator(bytes([CONST, 2, CONST, 3, ADD, CONST, 5, LT]))
# print(calc.execute())

# logging.shutdown()