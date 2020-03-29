from animus import animus_py3 as animus
from animus import animus_utils as utils
from flask import Flask, render_template, request, jsonify, make_response
import sys
import logging
import random
import cv2
# from animus import functionss
import time
import atexit
import signal

# animus.functionss.print9()
myrobot1 = None
log1 = None
# import sys
# sys.path.insert(0,'../animus/')
# sys.path.append('../animus')
# import animus.functionss as functionss

# import functionss
# functionss.print9()
# from animus import functionss
animus.version()
log = utils.create_logger("MyAnimusApp", logging.INFO)

success = animus.login_user("daniel@cyberselves.com", "cyberpass123")
if success:
    log.info("Logged in")
else:
    sys.exit(-1)

robots_found = animus.get_robots(True, True)

if len(robots_found) == 0:
    log.info("No robots available")
    sys.exit(-1)

for robot in robots_found:
    if robot.Available:
        available = "Robot Available"
    else:
        available = "Robot Unavailable"
    log.info("{}: {} robot from {} - {}".format(robot.Name, robot.Model, robot.Make, available))

my_robot_name = "Agnetha"
chosen_robot_details = None

for robot in robots_found:
    if robot.Name == my_robot_name:
        chosen_robot_details = robot

if chosen_robot_details is None:
    log.error("Please specify a valid robot name")
    sys.exit(-1)

myrobot2 = animus.Robot(chosen_robot_details)
connected = myrobot2.connect()
if not connected:
    print("Could not connect with robot {}".format(myrobot2.robot_details.ID))
    sys.exit(-1)
myrobot2.open_modality("emotion")
myrobot2.open_modality("speech")
myrobot2.set_modality("speech", " ")
myrobot2.set_modality("emotion", "neutral")
app = Flask(__name__)

# ../animus/app.py

@app.route("/")
def index():
    return render_template("index.html", token="From flask")


@app.route("/animus", methods=["GET"])
def animus_setup():
    try:
      global myrobot1
      global log1
      # (myrobot1,log1)=animus.functionss.setup1()
      # (myrobot1,log1)=animus.functionss.speechSetUp(myrobot1,log1)
      # (myrobot1,log1)=functionss.eyeColourSetup(myrobot1,log1)
    #   animus.functionss.visual(myrobot1,log1)
    #   myrobot1="success robot"
    #   log1="success log"
    #   time.sleep(2)
      print("finished setup")
    #   print(myrobot1)
    #   print(log1)
      time.sleep(2)
      res = make_response(jsonify({"message": "OK"}), 200)
      return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res



@app.route("/emotion-phrase", methods=["POST"])
def add_phrase():
    global myrobot2
    try:
        req = request.get_json()
        # message="Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World"
        # animus.functionss.speak(myrobot1,log1,req)
        myrobot2.set_modality("speech", req)
        emotion_list=['angry', 'fear', 'sad', 'happy', 'surprised']
        # print(random.choice(emotion_list))
        myrobot2.set_modality("emotion", random.choice(emotion_list))
        # myrobot2.set_modality("emotion", "angry")
        # animus.functionss.changeEyeColour(myrobot1,log1,random.choice(emotion_list))
        time.sleep(3)
        print(req)
        print("success")
        res = make_response(jsonify({"message": "OK"}), 200)
        return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res


def signal_handler(signal, frame):
  global myrobot2
  myrobot2.disconnect()
  animus.close_client_interface()
  print("closed connection")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# def close_running_threads():
#   global myrobot2
#   myrobot2.disconnect()
#   animus.close_client_interface()
#   print("closed connection")


#############

# @app.route("/brainstream", methods = ["POST"])
# def read_bci():
#     try:
#         goooo()
#     except:
#         print("no")

# def do_brain_stuff():
#     # await cortex.inspectApi()
#     print("** USER LOGIN **")
#     await cort.get_user_login()
#     print("** GET CORTEX INFO **")
#     await cort.get_cortex_info()
#     print("** HAS ACCESS RIGHT **")
#     await cort.has_access_right()
#     print("** REQUEST ACCESS **")
#     await cort.request_access()
#     print("** AUTHORIZE **")
#     await cort.authorize()
#     print("** GET LICENSE INFO **")
#     await cort.get_license_info()
#     print("** QUERY HEADSETS **")
#     await cortex.query_headsets()

# def goooo():
#     print("starting")
#     cort = Cortex('credentials.txt')
#     asyncio.run(do_brain_stuff(cort))
#     cort.close()

app.run(debug=True, use_reloader=False)
