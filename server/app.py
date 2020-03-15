import animus
from flask import Flask, render_template, request, jsonify, make_response
import sys
import logging
import random
import cv2
from animus import functionss
import time

animus.functionss.print9()
myrobot1 = None
log1 = None
# import sys
# sys.path.insert(0,'../animus/')
# sys.path.append('../animus')
# import animus.functionss as functionss

# import functionss
# functionss.print9()
# from animus import functionss


app = Flask(__name__)

# ../animus/app.py

@app.route("/")
def index():
    # (myrobot,log)=animus.functionss.setup1()
    # animus.functionss.speechSetUp(myrobot,log)
    # # message = input("type something")
    # message="Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World"
    # animus.functionss.speak(myrobot,log,message)
    # time.sleep(3)
    # animus.functionss.closeConnection(myrobot)
    return render_template("index.html", token="From flask")


@app.route("/animus", methods=["GET"])
def animus_setup():
    try:
      global myrobot1
      global log1
    #   (myrobot1,log1)=animus.functionss.setup1()
    #   animus.functionss.speechSetUp(myrobot1,log1)
    #   animus.functionss.visual(myrobot1,log1)
    #   myrobot1="success robot"
    #   log1="success log"
      time.sleep(2)
      print("it is sleeping")
    #   print(myrobot1)
    #   print(log1)
      
      res = make_response(jsonify({"message": "OK"}), 200)
      return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res



@app.route("/emotion-phrase", methods=["POST"])
def add_phrase():
    try:
        req = request.get_json()
        print(req)
        print("success")
        # message="Hello World Hello World Hello World Hello World Hello World Hello World Hello World Hello World"
        # animus.functionss.speak(myrobot1,log1,req)
        emotion_list=['angry', 'fear', 'sad', 'happy', 'surprised', 'neutral']
        # print(random.choice(emotion_list))
        # animus.functionss.changeEyeColour(myrobot1,log1,random.choice(emotion_list))
        # time.sleep(3)
        res = make_response(jsonify({"message": "OK"}), 200)
        return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res

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
