import os
import json
import serial
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
path=askopenfilename()


usb_port="COM10"
ser = serial.Serial(usb_port,baudrate=9600,timeout=1)






path= r'%s' % path
file="matrixanimastionmap.json"
print(path)
def main():#read json and save it into maplist as a list

    time.sleep(3)

    npath= "%s\%s" % (path,file)
    with open(path,"r")as filed:
        data=filed.read()
        dic=json.loads(data)
        for item in dic:
            time.sleep(0.5)
            maplist =dic[item]
            sendlist(maplist)






def sendlist(send):
    ser.write(bytearray([119,len(send)]))
    ser.write(bytearray(send))
    ser.flush()

        



while True:
    if __name__=="__main__":
        main()
