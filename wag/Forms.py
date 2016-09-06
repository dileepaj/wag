from wtforms import *
from wag.data.persistence.Persistence import Persistence

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, message = (u'Username is too short')),
                                      validators.Length(max=25, message = (u'Username is too long'))])
    password = PasswordField('Password', [validators.Length(min=1, message = (u'Password is too short')),
                                      validators.Length(max=15, message = (u'Password is too long'))])
    remember = BooleanField('Remember Me')
    def validate_on_submit(self):
        return
   
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, message = (u'Username is too short')),
                                      validators.Length(max=25, message = (u'Username is too long'))])
    email = TextField('Email',[
                           validators.Length(min=6, max=35, message=(u'Email address out of bounds')), 
                           validators.Email(message=(u'Not a valid email address'))] )
    password = PasswordField('Password', [validators.Length(min=1, message = (u'Password is too short')),
                                      validators.Length(max=15, message = (u'Password is too long'))])
    rePassword = PasswordField('Re-enter Password', [validators.Length(min=1, message = (u'Password is too short')),
                                      validators.Length(max=15, message = (u'Password is too long'))])
    
    userType = BooleanField('Paid User')
    #this checks username on submit, will be replaced with dynamic check
    def validate_username(form, field):
        #accessing db here, so a coupling is increased with the Data module.
        persist = Persistence()
        if persist.getUser(field.data) != None:
            #username exists in db
            raise ValidationError(u'Username already exists')
        
        
    def validate_rePassword(form, field):
        if field.data != form.password.data :
            raise ValidationError(u'The passwords doesn\'t match')    