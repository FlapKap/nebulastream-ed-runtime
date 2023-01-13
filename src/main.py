# main.py -- put your code here!
import json
import io
import logging
from sensors import Sensors
from connection import LoRaWAN

import protocol
import environment
import execution
import micropython
from unittest import unittest
from datatypes import pack_array
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
queries = protocol.decode_input_msg(msg)
logger.info("configuration recieved: {} operators".format(len(queries)))

logger.info("Starting main loop")
# The main loop is probably better off being in its own module/class for testability
while True:
    # set up pipe
    ## set up environment with first pull of sensor data
    sensor_readings = [s.pull() for s in sensors]
    query_responses = execution.execute_queries(queries, sensor_readings)
    
    #transmit result if any
    logger.debug("Checking if result needs to be transmitted")
    if all(map(lambda x: x is None or len(x) == 0, query_responses)):
        logger.debug("no queries with responses. Not transmitting anything")
        continue

    #gather results that needs to be transmitted
    responses = []
    for i, (query,resp) in enumerate(query_responses):
        #skip the empty ones
        if resp is None or len(resp) == 0:
            continue
        
        responses.append({"id": i, "response": pack_array(query.resultType,resp)})
        

    ##TODO: first we only assume a single value
    logger.debug("Transmitting result: {}".format(responses))
    output_msg = protocol.encode_output_msg({"responses":responses})
    lora.send(output_msg)

    #check if new messages are waiting
    if lora.data_waiting:
        #TODO: move this to its own method. Probably better with a connectionhandler class
        # that combines connection and protocol
        logger.info("Data Waiting. Loading new configuration")
        msg = lora.recieve_blocking()
        queries = protocol.decode_input_msg(msg)
        logger.info("configuration recieved: {} operators".format(len(queries)))
    

logging.shutdown()