from wag import app
from wag.data.persistence.Persistence import Persistence
from flask_login import LoginManager, make_secure_token, UserMixin
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_fresh
import md5, datetime

login_manager = LoginManager()

login_manager.init_app(app)
#the name of the view to login if a login_required page is accessed
login_manager.login_view = 'login'
login_manager.login_message = u'First login to access the page'
login_manager.login_message_category = 'info'
              
login_serializer = URLSafeTimedSerializer(app.secret_key)

class User(UserMixin):
    
    def __init__(self):
        self.id = "Guest"
        self.persistence = Persistence()
        self.authenticated = False
        self.anon = True
        self.type = "Free"
    
    def __init__(self, username, email, password, type):
        self.id = username
        self.email = email
        self.password = password
        self.persistence = Persistence()
        self.type = type
    
    @staticmethod    
    def get(userid):
        persistence = Persistence()
        user = persistence.getUser(userid.lower())
        if user:
           userObj = User(user['id'], user['email'], user['password'], user['type'])
           return userObj
        return user     
    
    def get_user(self, userid):
        return self.persistence.getUser(userid)
    
    def save(self):
        self.password = hash_pass(self.password)
        self.persistence.insertUser(self)
    
    def get_auth_token(self):
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

def hash_pass(password):
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@login_manager.token_loader
def load_token(token):
    
    max_age = app.config['REMEMBER_TOKEN_DURATION'].total_seconds()
    data = login_serializer.loads(token, max_age = max_age)
    user = User.get(data[0])
    if user and data[1] == user.password:
        return user
    return None
     
  