# main.py -- put your code here!
import socket
import json
import io
import logging
import time
from sensors import Sensors
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

## set up sensors
logger.info("initialising sensors...")
sensors = Sensors(config["sensors"])
logger.info("{} sensors initialized".format(sensors.sensor_count()))

# set up pipe
stack = Stack([2])
operations = [Map(Expression(bytes([CONST, INT8, 4, MUL]),stack=stack))]


for op in operations:
    logger.debug("oper: {}".format(op))
    op(stack=stack)



print(stack)
logging.shutdown()
# # set up connection

# logger.info("initialising connection")
# lora = LoRaWAN(lora_config["joineui"], lora_config["appkey"])
# logger.debug("hej")

# calc = Calculator(bytes([CONST, 2, CONST, 3, ADD, CONST, 5, LT]))
# print(calc.execute())

# logging.shutdown()