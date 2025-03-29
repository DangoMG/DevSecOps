from flask import Flask, request, render_template

app = Flask(__name__)

from flask import Flask, request, render_template, jsonify

# ... existing Flask setup ...

@app.route("/api/calc", methods=["POST"])
def api_calc():
    data = request.get_json()
    a = int(data["a"])
    b = int(data["b"])
    op = data["operation"]

    result = a + b if op == "add" else a - b
    return jsonify({"result": result})


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        a = int(request.form["a"])
        b = int(request.form["b"])
        operation = request.form["operation"]

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
