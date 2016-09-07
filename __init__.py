from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

# configuration
SECRET_KEY = '6lsqywSdlF6MYJAoNzbn-DTwaCnEa6jH'
# MONGODB_HOST = 'mongodb://rajika:intel@123@ds019746.mlab.com:19746/heroku_fqghj6dr'
# MONGODB_PORT = 19746
MONGO_URI = 'mongodb://rajika:intel@123@ds019746.mlab.com:19746/heroku_fqghj6dr'


app.secret_key = SECRET_KEY

import wag.Views
import wag.Forms