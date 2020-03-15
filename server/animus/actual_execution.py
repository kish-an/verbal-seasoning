import animus_py3 as animus
import animus_utils as utils
import sys
import logging
import random
import cv2
import functionss


functionss.print9()
(myrobot,log)=functionss.setup1()
print("finished set up")
functionss.visual(myrobot,log)
# # functionss.eyeColourSetup(myrobot,log)
# # functionss.changeEyeColour(myrobot,log,"angry")
# functionss.speechSetUp(myrobot,log)
# functionss.speak(myrobot,log,"Hello")
functionss.closeConnection(myrobot)