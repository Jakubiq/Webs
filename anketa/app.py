import sqlite3
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.debug = True
app.secret_key = "rakel420666"


class AnketaForm(FlaskForm):
    volba = RadioField(choices=[('volba1', 'C++'),
                                ('volba2', 'C#'),
                                ('volba3', 'JavaScrip'), 
                                ('volba4', 'Python')])


@app.route('/', methods=['GET', 'POST'])
def fnbattlepass():
    form = AnketaForm()
    hlas = form.volba.data
    if form.validate_on_submit():
        con = sqlite3.connect('anketa.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO anketa({hlas}) VALUES(1)")
        con.commit()
        con.close()
        return redirect('/hlasovano')
    return render_template('index.html', form=form)


@app.route('/hlasovano')
def hlasovano():
    con = sqlite3.connect('anketa.db')
    cur = con.cursor()
    cur.execute("SELECT SUM(volba1), SUM(volba2), SUM(volba3), SUM(volba4) FROM anketa;")
    vysledky = cur.fetchone()
    return render_template('hlasovano.html', vysledky=vysledky)



if __name__ == '__main__':
    app.run()
