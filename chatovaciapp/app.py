import sqlite3
from flask import Flask, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TimeField, TextAreaField


app = Flask(__name__)
app.debug = True
app.secret_key = "qwertz"

class chatForm(FlaskForm):
    jmeno = StringField("jméno")
    zprava = TextAreaField("zpráva")



@app.route('/', methods=['GET', 'POST'])
def chat():
    con = sqlite3.connect("chat.db")
    cur = con.cursor()
    cur.execute("SELECT jmeno,zprava FROM chat")
    zpravy = cur.fetchall()
    form = chatForm()
    chatJmeno = form.jmeno.data
    chatZprava = form.zprava.data
    if form.validate_on_submit():
        con = sqlite3.connect('chat.db')
        cur = con.cursor()
        cur.execute('INSERT INTO chat(jmeno, zprava) VALUES(?, ?)',
                    (chatJmeno, chatZprava))
        con.commit()
        con.close()
        session['prezdivka'] = chatJmeno
        return redirect('/')
    return render_template('chat.html', form=form, zpravy=zpravy)

@app.route('/odhlasit', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
