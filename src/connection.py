import time
import socket
import logging
import ubinascii
from network import LoRa

logger = logging.getLogger(__name__)


class LoRaWAN:

    def __init__(self, join_eui, app_key, region="EU868"):
        logger.info("initialise with join_eui:{0} app_key {1}".format(
            join_eui, app_key))
        self.join_eui = ubinascii.unhexlify(join_eui)
        self.app_key = ubinascii.unhexlify(app_key)
        if region == "EU868":
            self.region = LoRa.EU868
        else:
            logger.error(
                "region {0} not supported. Defaulting to EU868".format(region))
            self.region = LoRa.EU868
            # Asia = LoRa.AS923
            # Australia = LoRa.AU915
            # Europe = LoRa.EU868
            # United States = LoRa.US915
       
        # define lora object
        self.lora = LoRa(mode=LoRa.LORAWAN, region=self.region)
        self._data_waiting = False

        def handler():
            logger.debug("incoming data callback triggered")
            self._data_waiting = True

        self.lora.callback(trigger=LoRa.RX_PACKET_EVENT, handler=handler)

    @property
    def get_data_waiting(self):
        return self._data_waiting

    def connect(self):
        logger.info("connecting...")

        # cache for speed
        lora = self.lora
        # create an OTAA authentication parameters

        # join a network using OTAA (Over the Air Activation)
        lora.join(activation=LoRa.OTAA, auth=(
            self.join_eui, self.app_key), timeout=0)

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

    def send(self, data: bytes) -> None:
        logger.info("sending data")
        sock = self.sock
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        sock.setblocking(True)

        # send some data
        sock.send(data)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        sock.setblocking(False)

    def receive(self):
        # get any data received (if any...)
        data = self.sock.recv(256)
        return data

    def recieve_blocking(self):
        self.sock.setblocking(True)
        data = self.sock.recv(256)
        self.sock.setblocking(False)
        return data