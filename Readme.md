# NebulaStream End Device Runtime

## Testing
to support unit-tests the unittest, unittest-discover, argparse and fnmatch from micropython-lib has been added


## Possible Improvemnts

1. `mod` in python (and possibly micropython) behaves different for negative numbers than C (https://stackoverflow.com/questions/3883004/the-modulo-operation-on-negative-n-5umbers-in-python)

2. remove global variables
   
   Right now stack and environment used for expressions are global. 

   This is no problem for single-threaded execution but it is kind of coupled and if later multithreading is needed then it becomes a chore.


3. handle sensors that do not produce numerical output
   1. GPS produces tuples of numbers
   2. on/off sensors/buttons?
   3. are there sensors that produces string output?
   4. spectrums produce rows or matrices of numbers

### Error Handling
how do we handle

1. divide by zero
2. empty stack when not expected
3. empty environment when not expected
4. corrupt expression

### LoRa / LoRaWAN
1. Support msgs spanning multiple lora packets. To do this we must automatically calculate max packet size
   - revelant links:
     - https://docs.pycom.io/firmwareapi/pycom/network/lora/
     - https://lora-developers.semtech.com/documentation/tech-papers-and-guides/the-book/packet-size-considerations/
  