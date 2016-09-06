#from nose.tools import *
import unittest
#import Wag
import wag
import os.path
from wag.utils.DOMParser import *
from Settings import PROJECT_ROOT
from wag.core.Rules import Rules
from wag.core.RuleInterpreter import RuleInterpreter
from wag.core.RuleEvaluator import RuleEvaluator
from wag.core.Features import Features
from bs4 import BeautifulSoup

TEST_PAGE = 'wag/templates/ALSI.html'

class WagFlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        wag.app.config['TESTING'] = True
        self.app = wag.app.test_client() 
        print "Set up!"
        
    def tearDown(self):
        print "TEARDOWN"
        
    def login(self, username, password):
        return self.app.post('/login', data=dict(
             username = username,
             password = password),follow_redirects = True)
        
    def logout(self):
        return self.app.post('/logout', follow_redirects = True)
    
    def register(self, username, email, password, rePassword):
        return self.app.post('/register', data = dict(
              username = username,
              email = email,
              password = password,
              rePassword = rePassword), follow_redirects = True)

    
    def notest_login_logout(self):
        rv = self.login('wag_dummy', '1234')
        assert 'Logged in as wag_dummy' in rv.data
        
        rv = self.logout()
        #assert 'Enter your web site url' in rv.data
        rv = self.login('wag_dummy', '12346')
        assert 'Wrong Username or Password' in rv.data
        rv = self.login('wag_notit', '1234')
        assert 'Wrong Username or Password' in rv.data
        
    def notest_register(self):
        rv = self.register('wag_userx', 'wag@wag.com', '1234', '1234')
        assert 'Logged in as wag_userx' in rv.data
        self.logout()
        

class WagCoreTestCase(unittest.TestCase):
    def setUp(self):
        wag.app.config['TESTING'] = True
        self.app = wag.app.test_client() 
        print "Set up core tests!"
        
    def tearDown(self):
        print "Finish Core tests"
        
    def test_basic(self):
        print "I RAN"
        
    def test_initRuleInterpreter(self, ):
        ri = RuleInterpreter()
        assert ri.features.__len__() == 10 
        
class WagUtilTestCase(unittest.TestCase):
    
    def setUp(self):
        wag.app.config['TESTING'] = True
        self.app = wag.app.test_client()
        testfilePath = os.path.join(PROJECT_ROOT, TEST_PAGE)
        f = open(testfilePath, 'r')
        self.testPageContent = f.read()
        self.dom = getDOM(self.testPageContent) 
        print "Set up Util tests!"
        
    def tearDown(self):
        print "Finish Core tests"
        
    def test_get_line(self):
        Ruledummy = Rules()
        rule1 = Ruledummy.getRule('1')
        node = rule1(self.dom)
        lineNo = getLine(node[0], self.testPageContent )
        assert lineNo == 13
    
if __name__ == '__main__':
    unittest.main()

htmldoc = """<html>
<head>
<title></title>

<!-- Include jquery and sourceFile.js for WAG framework -->
<script type="text/javascript" src="lib/sourceFile.js"></script>

<link type="text/css" href="main.css" rel="stylesheet" />
</head>

<body>
    <div id="title">Advanced Level Science Institute</div>

    <div id="body">
        <div>
            <img src="image.jpg" width="40%">
            <p align="justify">
                We provide best learning materials online about the subjects under
                Advance Level Science stream. The subjects covered are <font
                    color="blue">Chemistry, Physics, Combined Mathematics and
                    Biology.</font> Our courses are designed following the standard syllabus
                by well experienced lecturers and teachers. The tutorials of each
                course include questions in similar pattern to the real advanced
                level examination.
            </p>
        </div>

        <div>
            <table id="table1" border="1">
                <tr>
                    <th>Time</th>
                    <th>Sunday</th>
                    <th>Monday</th>
                    <th>Tuesday</th>
                </tr>
                <tr>
                    <td>09 a.m. - 10 a.m.</td>
                    <td>Physics</td>
                    <td>Biology</td>
                    <td>Chemistry</td>
                </tr>
                <tr>
                    <td>01 p.m. - 03 p.m.</td>
                    <td>Chemistry</td>
                    <td>C. Maths</td>
                    <td>Physics</td>
                </tr>
                <tr>
                    <td>07 p.m. - 08 p.m.</td>
                    <td>Physics</td>
                    <td>Biology</td>
                    <td>Chemistry</td>
                </tr>
            </table>
        </div>

        <div>
            <div id="links">
                <h3>Useful Links:</h3>
                <a href="http://dir.yahoo.com/science/" tabindex='0'>http://dir.yahoo.com/science/</a>
                <br /> <a href="http://www.popsci.com/science" tabindex='0'>http://www.popsci.com/science</a>
                <br />
                <br /> <img src="num.jpg" width="50%" >
            </div>
            <div id="form">
                <h3>Sign Up:</h3>
                <label>Name </label> <input type="text" /> <br /> <label>e-mail
                </label> <input type="text" /> <br />
                <button ondblclick="alert('Welcome!!!');">Submit</button>
                <br />
            </div>
        </div>
    </div>

    <div id="footer"></div>

</body>
</html>"""     
    