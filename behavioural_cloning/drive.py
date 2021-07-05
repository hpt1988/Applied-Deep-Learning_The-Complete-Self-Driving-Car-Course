# Connection between the model and simulator

# We need to install a python Socket.io server
# --> Install Socket.io: pip install python-socketio
#                        conda install -c conda-forge python-socketio
import socketio

# conda install -c conda-forge eventlet
import eventlet

import numpy as np  # conda install -c anaconda numpy

# Initialize a Python web application
# --> Install Flask: pip install Flask
#                    conda install -c anaconda flask
# Flask is python micro framework that used to build web apps
# Goal: Create a bidirectional client-server communication
from flask import Flask  # To create instances of a web application

# conda install -c conda-forge tensorflow
# conda install -c conda-forge keras
from keras.models import load_model

import base64  # To decode base64 image
from io import BytesIO
from PIL import Image  # conda install -c anaconda pillow
import cv2

# Websockets in general are used to perform real-time communication
# between a client and a server.
# When a client creates a single connection to a websocket server, it
# keeps listening for new events from this server, allowing us to
# continuously update the client with data.
# In our case, we will be setting up a socket.io server, and stablish
# bi directional communication with the simulator. This server class
# implements a fully compliant socket.io web-server
sio = socketio.Server()

app = Flask(__name__)  # '__main__'

speed_limit = 10

# Image preprocessing function from previous course
def img_preprocess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255

    return img

# Registering a specific enevet handler
@sio.on('telemetry')
def telemetry(sid, data):
    speed = float(data['speed'])

    # Listening for updates that will be sent to the telemetry from the
    # simulator
    # Before we can open and identify the given image file with
    # image.open from the python imaging library (PIL), we need to use a
    # buffer module to mimic our data like a normal file, which we can
    # further use for processing. To do so, we use BytesIO
    # image is base64 encoded
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    throttle = 1.0 - speed / speed_limit
    print('{} {} {}'.format(steering_angle, throttle, speed))
    send_control(steering_angle, 1.0)

# Fire an event handler when there is a connection between the client
# Register an event handler.
# Event name is 'connect', it can also be 'message' and 'disconnect'
@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    send_control(0, 0)

def send_control(steering_angle, throttle):
    sio.emit('steer', data = {
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    })

if __name__ == '__main__':
    model = load_model('model.h5')

    # Middleware to dispatch traffic to a socket.io web application.
    # We will combine our socket.io server with a Flask web app
    app = socketio.Middleware(sio, app)

    # Web-server gateway interface, to have our web-server send any
    # request made by the client to the web application itself.
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)

# Running the current code in the simulator shows that the performance
# in the trained track is almost acceptable, but it is not performing
# well in the 2nd track, which means that our model has not learned to
# generalize to a new dataset.
# This issue will be resolved in the next lesson
