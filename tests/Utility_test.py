from nose.tools import *
from Wag.Server.Utility.DOMParser import *
from Wag.Server.Core.rules import Rules
from bs4 import BeautifulSoup

class DOMParser_Test:
    soup = None
    def setup(self):
        print "Set up!"
    
    def teardown(self):
        print "TEARDOWN"
        
    def test_getLine(self):
        rule = Rules()
        fullPage = BeautifulSoup(htmldoc)
        node = rule.rule1(fullPage)
        print getLine(node[0], htmlraw)
        eq_(getLine(node[0], htmlraw),16)
        
htmlraw = """<!DOCTYPE html>\n<html>\n<head>\n<title></title>\n\n<!-- Include jquery and sourceFile.js for WAG framework -->\n<script type=\"text/javascript\" src=\"lib/sourceFile.js\"></script>\n\n<link type=\"text/css\" href=\"main.css\" rel=\"stylesheet\" />\n</head>\n\n<body>\n\t<div id=\"title\">Advanced Level Science Institute</div>\n\n\t<div id=\"body\">\n\t\t<div>\n\t\t\t<img src=\"image.jpg\" width=\"40%\"/>\n\t\t\t<p align=\"justify\">\n\t\t\t\tWe provide best learning materials online about the subjects under\n\t\t\t\tAdvance Level Science stream. The subjects covered are <font\n\t\t\t\t\tcolor=\"blue\">Chemistry, Physics, Combined Ma
thematics and\n\t\t\t\t\tBiology.</font> Our courses are designed following the
standard syllabus\n\t\t\t\tby well experienced lecturers and teachers. The tutor
ials of each\n\t\t\t\tcourse include questions in similar pattern to the real ad
vanced\n\t\t\t\tlevel examination.\n\t\t\t</p>\n\t\t</div>\n\n\t\t<div>\n\t\t\t<
table id=\"table1\" border=\"1\">\n\t\t\t\t<tr>\n\t\t\t\t\t<th>Time</th>\n\t\t\t
\t\t<th>Sunday</th>\n\t\t\t\t\t<th>Monday</th>\n\t\t\t\t\t<th>Tuesday</th>\n\t\t
\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td>09 a.m. - 10 a.m.</td>\n\t\t\t\t\t<td>Phy
sics</td>\n\t\t\t\t\t<td>Biology</td>\n\t\t\t\t\t<td>Chemistry</td>\n\t\t\t\t</t
r>\n\t\t\t\t<tr>\n\t\t\t\t\t<td>01 p.m. - 03 p.m.</td>\n\t\t\t\t\t<td>Chemistry<
/td>\n\t\t\t\t\t<td>C. Maths</td>\n\t\t\t\t\t<td>Physics</td>\n\t\t\t\t</tr>\n\t
\t\t\t<tr>\n\t\t\t\t\t<td>07 p.m. - 08 p.m.</td>\n\t\t\t\t\t<td>Physics</td>\n\t
\t\t\t\t<td>Biology</td>\n\t\t\t\t\t<td>Chemistry</td>\n\t\t\t\t</tr>\n\t\t\t</t
able>\n\t\t</div>\n\n\t\t<div>\n\t\t\t<div id=\"links\">\n\t\t\t\t<h3>Useful Lin
ks:</h3>\n\t\t\t\t<a href=\"http://dir.yahoo.com/science/\" tabindex='0'>http://
dir.yahoo.com/science/</a>\n\t\t\t\t<br /> <a href=\"http://www.popsci.com/scien
ce\" tabindex='0'>http://www.popsci.com/science</a>\n\t\t\t\t<br />\n\t\t\t\t<br
 /> <img src=\"num.jpg\" width=\"50%\">\n\t\t\t</div>\n\t\t\t<div id=\"form\">\n
\t\t\t\t<h3>Sign Up:</h3>\n\t\t\t\t<label>Name </label> <input type=\"text\" />
<br /> <label>e-mail\n\t\t\t\t</label> <input type=\"text\" /> <br />\n\t\t\t\t<
button ondblclick=\"alert('Welcome!!!');\">Submit</button>\n\t\t\t\t<br />\n\t\t
\t</div>\n\t\t</div>\n\t</div>\n\n\t<div id=\"footer\"></div>\n\n</body>\n</html
>"""

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