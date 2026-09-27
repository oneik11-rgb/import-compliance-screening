from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Import Compliance Screening System - Unit 4 Prototype"


if __name__ == "__main__":
    app.run(debug=True)