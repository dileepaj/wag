#from nose.tools import *
import unittest
#import Wag
from wag import app

class WagTestCase(unittest.TestCase):
    def setup():
        app.config['TESTING'] = True
        print "Set up!"
        
    def teardown():
        print "TEARDOWN"
        
    def test_basic():
        print "I RAN"
        
    def login(self, username, password):
        return self.app.post('/login', data=dict(
             username = username,
             password = password),follow_redirects = True)
        
    def logout(self):
        return self.app.post('/logout', follow_redirects = True)
    
if __name__ == '__main__':
    unittest.main()
    
    