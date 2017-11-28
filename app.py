import json
import flask

from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import flask
import pandas as pd

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = 'mystery'

class DataFile(FlaskForm):
    name = StringField('File to load',validators=[Required()])
    desc = StringField('Description')
    submit = SubmitField('Press go')

@app.before_first_request
def before_first(*args, **kwargs):
    session['data'] = None
    session['data_old'] = None

@app.route("/", methods=['GET', 'POST'])
def index():
    form = DataFile()
    if form.validate_on_submit():
        if session['data']:
            session['data_old'] = session['data']

        df = pd.read_csv(form.name.data).drop('Open', axis=1)
        chart_data = df.to_dict(orient='records')
        chart_data = json.dumps(chart_data, indent=2)
        session['data'] = {'chart_data': chart_data}
        desc = form.desc.data
    else:
        session["data"] = None
        desc = None

    return render_template("index.html",
        filename_form=form,
        data=session["data"],
        data_old=session["data_old"],
        desc=desc)

if __name__ == "__main__":
    app.run(debug=True)
