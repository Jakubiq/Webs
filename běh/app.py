import sqlite3
from flask import Flask, redirect, render_template
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import IntegerField, StringField, TimeField, TextAreaField


app = Flask(__name__)
app.debug = True
app.secret_key = "sdv sv  dfs df2456345646"


class ZavodnikForm(FlaskForm):
    jmeno = StringField("jméno", validators=[InputRequired()])
    prijmeni = StringField("příjmení", validators=[InputRequired()])
    cislo = IntegerField("startovní číslo", validators=[InputRequired()])
    cas = TimeField("čas", format='%H:%M:%S', validators=[InputRequired()])
    poznamka = TextAreaField("poznámka")


@app.route('/')
def vysledky():
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM beh")
    vysledky = cur.fetchall()
    con.close()
    return render_template('vysledky.html', vysledky=vysledky)



@app.route('/pridat', methods=['GET', 'POST'])
def vloz():
    form = ZavodnikForm()
    zavodnik_jmeno = form.jmeno.data
    zavodnik_prijmeni = form.prijmeni.data
    zavodnik_cislo = form.cislo.data
    zavodnik_cas = str(form.cas.data)
    zavodnik_poznamka = form.poznamka.data
    if form.validate_on_submit():
        con = sqlite3.connect('beh.db')
        cur = con.cursor()
        cur.execute('INSERT INTO beh(jmeno, prijmeni, cislo, cas, poznamka) VALUES(?, ?, ?, ?, ?)',
                    (zavodnik_jmeno, zavodnik_prijmeni, zavodnik_cislo, zavodnik_cas, zavodnik_poznamka))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('zavodnik.html', form=form)

@app.route('/prijmeni')
def prijmeni():
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM beh ORDER BY prijmeni")
    vysledky = cur.fetchall()
    title = "Seřazení podle příjmení"
    con.close()
    return render_template('vysledkyPrijmeni.html', vysledky=vysledky, title=title)

@app.route('/prijmeniDesc')
def prijmeniDesc():
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM beh ORDER BY prijmeni DESC")
    vysledky = cur.fetchall()
    title = "Seřazení podle příjmení sestupně"
    con.close()
    return render_template('vysledkyPrijmeni.html', vysledky=vysledky, title=title)

@app.route('/cas')
def cas():
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM beh ORDER BY cas")
    vysledky = cur.fetchall()
    title = "Čas od nejrychlejšího"
    con.close()
    return render_template('vysledkyCas.html', vysledky=vysledky, title=title)

@app.route('/casDesc')
def casDesc():
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("SELECT cislo, prijmeni, jmeno, cas FROM beh ORDER BY cas DESC")
    vysledky = cur.fetchall()
    con.close()
    title = "Čas od nejpomalejší"
    return render_template('vysledkyCas.html', vysledky=vysledky, title=title)

@app.route('/odstranit/<int:id_zavodnika>')
def remove(id_zavodnika):
    con = sqlite3.connect("beh.db")
    cur = con.cursor()
    cur.execute("DELETE FROM beh WHERE cislo=?", (id_zavodnika,))
    con.commit()
    con.close()
    return render_template('vysledky.html', vysledky=vysledky)


if __name__ == '__main__':
    app.run()
