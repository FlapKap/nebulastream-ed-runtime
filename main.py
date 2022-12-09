# main.py -- put your code here!
import socket
import json
import io
import logging
import time

# load config
config = json.load(io.open("config.json", mode='r'))

loglevel = {"info": logging.INFO, "warning": logging.WARNING,
            "debug": logging.DEBUG, "error": logging.ERROR}[config["loglevel"].tolower()]
logging.basicConfig(level=loglevel)
logger = logging.getLogger(__name__)

logger.info("config loaded")
