from flask import Flask, render_template

app = Flask(__name__)


# @app.route("/")
# def hello():
#     return "Hello World!"


@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/form/')
def form():
    return render_template('form.html')


# @app.route('/products/')
# def products():
#     return render_template('products.html')


@app.route('/results/')
def results():
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)
