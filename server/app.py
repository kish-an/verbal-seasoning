from flask import Flask, render_template, request, jsonify, make_response

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

app.run(debug=True)
