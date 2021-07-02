# Connection between the model and simulator

# Initialize a Python web application
# --> Install Flask
# Flask is python micro framework that used to build web apps
from flask import Flask  # To create instances of a web application

app = Flask(__name__)  # '__main__'

@app.route('/home')
def greeting():
    return 'Welcome!'

if __name__ == '__main__':
    app.run(port=3000)  # Arbitrary value

# We need to install a python Socket.io server
