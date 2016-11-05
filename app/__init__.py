#!/usr/bin/env python
from flask import Flask, render_template, Response, send_file, request, redirect, url_for

# emulated camera
try: from .camera_pi import Camera
except: from .camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
camera = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    fname = camera.snapshot(app.static_folder)
    static_url = url_for('static', filename=fname)
    print(static_url)
    return redirect(static_url)
    
@app.route('/settings', methods=['GET'])
def settings():
    args = request.args.to_dict()
    x,y = args.pop('x'), args.pop('y')
    args['resolution'] = (x, y)
    camera.settings = args
    print(request.args)
    print(args)
    return index()
