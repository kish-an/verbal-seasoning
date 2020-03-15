import sys
import logging
import random
import cv2
from animus import functionss
import time


functionss.print9()
(myrobot,log)=functionss.setup1()
print("finished set up")
# functionss.visual(myrobot,log)
# functionss.eyeColourSetup(myrobot,log)
# functionss.changeEyeColour(myrobot,log,"angry")
# time.sleep(3)
functionss.speechSetUp(myrobot,log)
# message = input("type something")
message="Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World"
functionss.speak(myrobot,log,message)
time.sleep(3)
functionss.closeConnection(myrobot)