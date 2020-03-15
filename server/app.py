from flask import Flask, render_template, request, jsonify, make_response
# import sys
# # sys.path.insert(0,'../animus/')
# sys.path.append('../animus')
# import animus.functionss as functionss

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
        # functionss.print9()
        print('------------------------------------')

        res = make_response(jsonify({"message": "OK"}), 200)
        return res
    except:
        res = make_response(jsonify({"message": "SERVER ERROR"}), 500)
        return res

app.run(debug=True)
