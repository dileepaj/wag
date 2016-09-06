from bs4 import BeautifulSoup
import re
import unicodedata
import selenium.webdriver
import os.path
from wag import app
from Settings import PROJECT_ROOT
from wag.utils.Constants import *
import urllib

def getDOM(content):
    try:
        soup = BeautifulSoup(content)
        return soup
    except :
        print "Parsing Error"
        return "Error"

def getLine(soupNode, Content):
    srsCode = getParsedContent(Content)  
    nodeString = str(soupNode)
    #nodeString = nodeString.replace("\"", "\\\"")
    index = srsCode.find(nodeString)
    if( index != -1 ):
        untilSlice = srsCode[0:index]
        line = untilSlice.count('\n')
        #because bs4 removes whitespace lines.
        #extraLines = untilSlice.count('\n\n')
        return line + 1 

def getParsedContent(content):
    return str(getDOM(content))
   
def getStrfromDOM(soupNode):
    soupString = str(soupNode)
    normalString = soupString.replace("\\\"", "").replace("\'", "\"")
    return normalString

def getContentStringfromNode(soupNode, content):
    line = getLine(soupNode, content)
    linesInNode = str(soupNode).count('\\n')
    totalLines = content.split('\\n')
    elemLine = '\\n'.join((totalLines[line:line+linesInNode+1]))
    return elemLine

def getNodeLineCount(elem):
    return elem.count('\\n')
        
def indexAtLine(content, line):
    nodeStartLine = 0
    index = 0
    while(nodeStartLine < line):
        if (content[index:].find('\\n') != -1):
            index = index + content[index:].find('\\n') + 2
            nodeStartLine = nodeStartLine + 1
        else : print "Something is wrong"
    return index


def convertToStr(uniStr):
    return unicodedata.normalize('NFKD', uniStr).encode('ascii', 'ignore')
    
def getFullyGeneratedHTML(url):
    phantomPath = os.path.join(PROJECT_ROOT, PHANTOMJS_EXE)
    driver = selenium.webdriver.PhantomJS(phantomPath)
    try:
        urllip.urlopen(url)
        driver.get(url)
        return driver.page_source
    except:
        raise IOError
    
        
    