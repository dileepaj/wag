from flask import json
from wag.utils.DOMParser import getFullyGeneratedHTML

class Page:
    def __init__(self, url = " ", content = "Nothing", disability = None, priority = None):
        self.homeUrl = url
        self.url = url
        self.content =  content
        self.disability = disability
        if priority:
            self.priority = int(priority)
        else: 
            self.priority = priority
        self.evaluationResults = None
    
    def setURL(self, url):
        self.url = url
        
    def setHomeUrl(self, url):
        self.homeUrl = url
    
    def setContent(self, content):
        try:
           print "getting full content"
           self.content = getFullyGeneratedHTML(self.url)
        except:
           print "can't access url"
           self.content = content
        
    def setPriority(self, priority):
        self.priority = int(priority)
        
    def setDisability(self,vals):
        self.disability = vals
        
    def getDisability(self):
        total = 1
        for v in self.disability:
            total = total * int(v)
        return total
    
    def setDisabilitiesfromVal(self, value):
        val = int(value)
        allVals = []
        if val % 5 == 0:
            allVals.append(u'5')
        if val % 3 == 0:
            allVals.append(u'3')
        if val % 2 == 0:
            allVals.append(u'2')
        
        self.disability = allVals    
                