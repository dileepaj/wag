from nose.tools import *
from Wag.Server.Core.ruleInterpreter import RuleInterpreter
from bs4 import BeautifulSoup


class ruleInterpreter_Test:
    soup = None
    def setup(self):
        print "Set up!"
    
    def teardown(self):
        print "TEARDOWN"

    def test_ruleInterpreter_init(self):
        ri = RuleInterpreter()
        assert True
        
    def test_makeFeatureCollection_TITLE(self):
        ri = RuleInterpreter()
        eq_(len(ri.features), 10)
        
        self.soup = BeautifulSoup("<TITLE>Express the meaning of color cues</TITLE>", 'xml')
        eq_(ri.features[2].title, self.soup.TITLE ) 
        assert True
        

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

    

    