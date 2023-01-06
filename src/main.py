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

if config["run_test"]:
    logger.info("test true. Running tests...")
    unittest.main(tests)
    import sys
    sys.exit()



## set up sensors
logger.info("initialising sensors...")
sensors = Sensors(config["sensors"])
logger.info("{} sensors initialized".format(sensors.sensor_count()))


# # set up connection

logger.info("initialising connection")
lora = LoRaWAN(lora_config["joineui"], lora_config["appkey"])
lora.connect()
logger.info("waiting for incoming configuration...")
msg = lora.recieve_blocking()
operations = protocol.decode_input_msg(msg)
logger.info("configuration recieved: {} operators".format(len(operations)))

logger.info("Starting main loop")
while True:
    # set up pipe
    ## set up environment with first pull of sensor data
    environment.replace_environment([s.pull() for s in sensors])
    logger.debug("environment initialized with sensor pull: {}".format(environment.get_environment()))
    
    res = None
    for op in operations:
        ## so far each operation gets its own stack
        ## TODO: this can probably be optimized away. Output of previous stack is input to next
        ## however cleaning the stack every time makes it a bit easier to reason about
        environment.clear_stack()
        logger.debug("oper: {} called with input: {}".format(op, res))
        res = op(res)
    
    #transmit result if any
    logger.debug("Checking if result needs to be transmitted")
    if res is not None:
        ##TODO: first we only assume a single value
        logger.debug("Transmitting result: {}".format(res))
        output_msg = protocol.encode_output_msg({"values": [{"key":0, "value":res}]})
        lora.send(output_msg)

    #check if new messages are waiting
    if lora.data_waiting:
        #TODO: move this to its own method. Probably better with a connectionhandler class
        # that combines connection and protocol
        logger.info("Data Waiting. Loading new configuration")
        msg = lora.recieve_blocking()
        operations = protocol.decode_input_msg(msg)
        logger.info("configuration recieved: {} operators".format(len(operations)))
    

logging.shutdown()