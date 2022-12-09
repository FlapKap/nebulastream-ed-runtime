import time
import socket
import logging
import ubinascii
from network import LoRa

logger = logging.getLogger(__name__)

class LoRaWAN:

    def __init__(self, join_eui, app_key):
        logger.info("initialise with join_eui:{0} app_key {1}".format(join_eui, app_key))
        self.join_eui = ubinascii.unhexlify(join_eui)
        self.app_key  = ubinascii.unhexlify(app_key)
        

        # Initialise LoRa in LORAWAN mode.
        # Please pick the region that matches where you are using the device:
        # Asia = LoRa.AS923
        # Australia = LoRa.AU915
        # Europe = LoRa.EU868
        # United States = LoRa.US915
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    def connect(self):
        logger.info("connecting...")
        #cache for speed
        lora = self.lora
        # create an OTAA authentication parameters
        

        # join a network using OTAA (Over the Air Activation)
        lora.join(activation=LoRa.OTAA, auth=(self.join_eui, self.app_key), timeout=0)

        # wait until the module has joined the network
        while not lora.has_joined():
            time.sleep(2.5)
            logger.debug("not connected yet...")

        # create a LoRa socket
        self.sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        sock = self.sock
        # set the LoRaWAN data rate
        sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        logger.info("connected")

    def send(self, data):
        logger.info("sending data")
        sock = self.sock
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        sock.setblocking(True)

        # send some data
        sock.send(bytes([0x01, 0x02, 0x03]))

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        sock.setblocking(False)


    def receive(self):
        # get any data received (if any...)
        data = self.sock.recv(64)
        return data

