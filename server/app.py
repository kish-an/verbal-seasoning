from flask import Flask, render_template, request, jsonify, make_response
import asyncio
from cortex import Cortex

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", token="From flask")

@app.route("/input", methods=["POST"])
def robot_talk():
    try:
        req = request.get_json()
        
        print('------------------------------------')
        print(req)
        print('------------------------------------')

        res = make_response(jsonify({"message": "OK"}), 200)
        return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res

#############

@app.route("/brainstream", methods = ["POST"])
def read_bci():
    try:
        goooo()
    except:
        print("no")

def do_brain_stuff:
    # await cortex.inspectApi()
    print("** USER LOGIN **")
    await cort.get_user_login()
    print("** GET CORTEX INFO **")
    await cort.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cort.has_access_right()
    print("** REQUEST ACCESS **")
    await cort.request_access()
    print("** AUTHORIZE **")
    await cort.authorize()
    print("** GET LICENSE INFO **")
    await cort.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()

def goooo():
    print("starting")
    cort = Cortex('credentials.txt')
    asyncio.run(do_brain_stuff(cort))
    cort.close()

app.run(debug=True)
