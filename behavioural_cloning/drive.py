# Connection between the model and simulator

# We need to install a python Socket.io server
# --> Install Socket.io: pip install python-socketio
import socketio

import eventlet

# Initialize a Python web application
# --> Install Flask: pip install Flask
# Flask is python micro framework that used to build web apps
# Goal: Create a bidirectional client-server communication
from flask import Flask  # To create instances of a web application

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

# Fire an event handler when there is a connection between the client
# Register an event handler.
# Event name is 'connect', it can also be 'message' and 'disconnect'
@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    send_control(0, 1)

def send_control(steering_angle, throttle):
    sio.emit('steer', data = {
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    })

if __name__ == '__main__':
    # Middleware to dispatch traffic to a socket.io web application.
    # We will combine our socket.io server with a Flask web app
    app = socketio.Middleware(sio, app)

    # Web-server gateway interface, to have our web-server send any
    # request made by the client to the web application itself.
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
