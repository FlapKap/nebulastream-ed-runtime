from messages import *
from messages import ExpressionInstructions as Einstr
from messages import ExpressionTypes as Etype

if __name__ == "__main__":
    msg =Message(MapOperation(
            Expression(bytes([Einstr.CONST, Etype.INT8,3,Einstr.CONST, Etype.INT8,9,Einstr.ADD]))
            ))
            
    print(msg.SerializeToString())