# main.py -- put your code here!
import json
import io
import logging
import time
import gc
from sensors import Sensors
from connection import LoRaWAN
import pycom
import protocol
import environment
import execution
import micropython
from unittest import unittest
from datatypes import pack_array, pack_type, INT32
import tests

# set compilation optimization level
micropython.opt_level(0) # no optimization. __debug__ = True
## allocate buffer space for emergency exceptions
micropython.alloc_emergency_exception_buf(100)
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
lora = LoRaWAN(lora_config["joineui"], lora_config["deveui"], lora_config["appkey"])
gc.collect()
logger.info("free heap: " +str(pycom.get_free_heap()))
lora.connect()
logger.info("waiting for incoming configuration...")
## dont know why but we have to send before it works
lora.send(b'a')
msg = lora.recieve_blocking()
logger.info("msg recieved: " + str(msg))
#msg = lora.recieve_blocking()
queries = protocol.decode_input_msg(msg)
logger.info("configuration recieved: {} queries".format(len(queries)))
logger.info("queries recieved: ")
for q in queries:
    logger.info(q)
logger.info("Starting main loop")
# The main loop is probably better off being in its own module/class for testability
while True:
    logger.debug("Main loop iteration")
    # set up pipe
    ## set up environment with first pull of sensor data
    sensor_readings = [s.pull() for s in sensors]
    logger.debug("\tsensor_readings={}".format(sensor_readings))
    query_results = execution.execute_queries(queries, sensor_readings)
    logger.debug("\tquery_results={}".format(query_results))
    #transmit result if any
    logger.debug("\tChecking if result needs to be transmitted")
    if all(map(lambda x: x is None or len(x) == 0, query_results)):
        logger.debug("\tno queries with responses. Not transmitting anything")
        continue

    logger.debug("\tgather results that needs to be transmitted")
    responses = []
    for i, (query,resp) in enumerate(zip(queries,query_results)):
        #skip the empty ones
        if resp is None or len(resp) == 0:
            continue
        
        responses.append({"id": i, "response": [pack_type(typ,res) for (typ,res) in zip(query.resultType, resp)] })
        

    ##TODO: first we only assume a single value
    logger.debug("\tTransmitting result: {}".format(responses))
    output_msg = protocol.encode_output_msg({"responses":responses})
    lora.send(output_msg)

    logger.debug("\tcheck for new config")
    data = lora.receive()
    if len(data)> 0:
        logger.info("\tconfig recieved")
        msg = lora.recieve_blocking()
        queries = protocol.decode_input_msg(msg)
        logger.info("configuration recieved: {} operators".format(len(queries)))
    #check if new messages are waiting
    # if lora.data_waiting:
    #     #TODO: move this to its own method. Probably better with a connectionhandler class
    #     # that combines connection and protocol
    #     logger.info("Data Waiting. Loading new configuration")
    #     msg = lora.recieve_blocking()
    #     queries = protocol.decode_input_msg(msg)
    #     logger.info("configuration recieved: {} operators".format(len(queries)))
    time.sleep(5)

logging.shutdown()