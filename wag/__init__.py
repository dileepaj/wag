from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

# configuration
SECRET_KEY = 'QqP@t5Boj`B#KAY~*Xs^z4kUGp04^{UDLV-V9%(m(0f4n+I M{7sMG)Zb?f#R7*x'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app.secret_key = SECRET_KEY

import wag.Views