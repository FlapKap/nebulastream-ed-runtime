# NebulaStream End Device Runtime

## Testing
to support unit-tests the unittest, unittest-discover, argparse and fnmatch from micropython-lib has been added


## TODO

1. handle sensors that do not produce numerical output
   1. GPS produces tuples of numbers
   2. on/off sensors/buttons?
   3. are there sensors that produces string output?
   4. spectrums produce rows or matrices of numbers

### LoRa / LoRaWAN
1. Support msgs spanning multiple lora packets. To do this we must automatically calculate max packet size
   - revelant links:
     - https://docs.pycom.io/firmwareapi/pycom/network/lora/
     - https://lora-developers.semtech.com/documentation/tech-papers-and-guides/the-book/packet-size-considerations/
  