from flask import Flask, render_template

app = Flask(__name__)


@app.route('/calc_damage')
def main():
    return "over 9000"


if __name__ == "__main__":
    app.run()
