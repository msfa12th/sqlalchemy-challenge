from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/members")
def members():
    return "Members"

@app.route("/members/<string:fname>/<string:lname>")
def getMember(fname,lname):
    return f"Hi My name is {fname} {lname}"

if __name__ == "__main__":
    app.run()
