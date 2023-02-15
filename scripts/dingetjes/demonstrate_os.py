"""Demonstrate library os"""

import os

home = os.getcwd()
print(os.listdir(home))

myDoc = os.path.join(home, "test.txt")
myString = "Dit is een test."
print(os.path.isfile(myDoc))

myFile = os.open(myDoc, os.O_APPEND | os.O_CREAT)
os.write(myFile, myString.encode())
os.close(myFile)
