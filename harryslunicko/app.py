import requests
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.debug = True


@app.route('/')
def Weather():
    city = "Praha"
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b77748418d25e708cc4f30931fc06401&units=metric&lang=cz'
    reply = requests.get(url).json()
    temp = reply['main']['temp']
    describe = reply['weather'][0]['description']
    icon = reply['weather'][0]['icon']
    return render_template('index.html', reply=reply, temp=temp, describe=describe, icon=icon)


if __name__ == '__main__':
    app.run()
