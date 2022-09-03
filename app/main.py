from flask import Flask, render_template, request

from hh_json import parce

from crud import add_row

app = Flask(__name__)


@app.get('/')
@app.get('/index/')
def index():
    return render_template('index.html')


@app.route('/form/')
def form():
    return render_template('form.html')


@app.post('/results/')
def results_post():
    """

    :return:
    """
    vacancies = request.form
    print(vacancies)
    data = parce(**vacancies)
    print(data)
    data_all = {**data, **vacancies}
    print(data_all)
    add_row(data_all)
    return render_template('results.html', res=data_all)


if __name__ == "__main__":
    app.run(debug=True)
