from flask import Flask, render_template, Response, jsonify, flash, redirect, request, url_for
import gunicorn
from camera import *
import os

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
headings = ("Name", "Album", "Artist")
df1 = music_rec()
df1 = df1.head(15)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        if login == 'ygrick' and password == 'admin':
            return redirect(url_for('index'))
        else:
            flash('Login or password is not correct')

    return render_template('login.html')

@app.route('/index')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    while True:
        global df1
        camera.get_frame()
        frame, df1 = camera.jpeg, camera.df1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')


if __name__ == '__main__':
    app.debug = True
    app.run()
