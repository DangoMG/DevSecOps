from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/add", methods=["GET"])
def add():
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    return jsonify(result=a + b)

@app.route("/subtract", methods=["GET"])
def subtract():
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    return jsonify(result=a - b)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
