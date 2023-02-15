import os

home = os.getcwd()
myPath = os.path.join(home, "test.txt")

myFile = open(myPath, "a")

for i in range(10):
    myStr = str(i)
    myFile.write(myStr + "\n")
