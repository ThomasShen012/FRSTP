from flask import Flask, render_template, url_for, request, session, redirect, Response
import json
import pymongo
from functools import wraps
from  flask_login import  login_user, login_required, logout_user, current_user
from user.camera import VideoCamera
import cv2

app = Flask(__name__)
app.secret_key = b'kushfuii7w4y7ry47ihwiheihf8774sdf4'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
        
    return wrap

video_stream = VideoCamera()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#routes
from user import routes

@app.route('/')
def home():
    return render_template('newhome.html')

@app.route('/user/register')
def user_signup():
    return render_template('register (1).html')

@app.route('/user/login')
def user_login():
    return render_template('loginnn.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/user/update_user')
@login_required
def edit():
    return render_template('update_user.html')

@app.route('/camera')
def camara():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    print(type(gen(video_stream)))
    print(gen(video_stream))
    
    return Response(gen(video_stream),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)