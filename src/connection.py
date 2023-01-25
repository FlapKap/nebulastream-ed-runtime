import time
import socket
import logging
import ubinascii
from network import LoRa

logger = logging.getLogger(__name__)


class LoRaWAN:

    def __init__(self, join_eui,dev_eui, app_key, region="EU868"):
        logger.info("initialise with join_eui:{0} dev_eui:{1} app_key: {2}".format(
            join_eui, dev_eui, app_key))
        self.join_eui = ubinascii.unhexlify(join_eui)
        self.dev_eui = ubinascii.unhexlify(dev_eui)
        self.app_key = ubinascii.unhexlify(app_key)
        self.sock = None
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
       


    def connect(self):
        logger.info("connecting...")
        # define lora object
        self.lora = LoRa(mode=LoRa.LORAWAN, region=self.region, power_mode=LoRa.ALWAYS_ON, device_class=LoRa.CLASS_C)
        self.data_waiting = False


        # create an OTAA authentication parameters

        # join a network using OTAA (Over the Air Activation)
        self.lora.join(activation=LoRa.OTAA, auth=(
             self.dev_eui, self.join_eui, self.app_key), timeout=0)

        logger.info("waiting for connection")
        # wait until the module has joined the network
        while not self.lora.has_joined():
            time.sleep(2.5)
            logger.debug("not connected yet...")

        # create a LoRa socket
        if not self.sock:
            self.sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
            # set the LoRaWAN data rate
            self.sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
            self.sock.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, 1)
            
            self.sock.setblocking(False)

        # def lora_cb(lora):
        #     events = lora.events()
        #     if events & LoRa.RX_PACKET_EVENT:
        #         if self.sock is not None:
        #             frame, port = self.sock.recvfrom(512) # longuest frame is +-220
        #             print(port, frame)
        #     if events & LoRa.TX_PACKET_EVENT:
        #         print("tx_time_on_air: {} ms @dr {}", lora.stats().tx_time_on_air, lora.stats().sftx)


        # self.lora.callback(trigger=(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT | LoRa.TX_FAILED_EVENT), handler=lora_cb)

        logger.info("connected")
        time.sleep(4)

    def send(self, data: bytes) -> None:
        logger.info("sending data")
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        self.sock.setblocking(True)

        # send some data
        self.sock.send(data)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        self.sock.setblocking(False)

    def receive(self):
        # get any data received (if any...)
        data = self.sock.recvfrom(255)
        print(str(data))
        return data[0]

    def recieve_blocking(self):
        logger.debug("receive_blocking called")
        data = self.sock.recv(255)
        while len(data) == 0:
            time.sleep_ms(1000)
            data = self.sock.recv(255)
        # if self.data_waiting:
        #     data = self.sock.recv(256)
        # else:
        #     self.sock.setblocking(True)
        #     data = self.sock.recv(256)
        #     self.sock.setblocking(False)
        print(data)
        return data