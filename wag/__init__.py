from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

# configuration
SECRET_KEY = '6lsqywSdlF6MYJAoNzbn-DTwaCnEa6jH'

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app.secret_key = SECRET_KEY

import wag.Views