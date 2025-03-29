from flask import Flask, request, render_template

app = Flask(__name__)

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
