from wag.utils import DOMParser
from RuleEvalResult import EvalResults
from Page import Page
from bs4 import BeautifulSoup

class RuleEvaluator(object):
    issues = []
    ruleInterpreter = None
        
    def __init__(self, ruleInterpreter):
        self.ruleInterpreter = ruleInterpreter
        self.priority = 3
        self.disability = [2,3,5]
        #self.page = None
       
    #def setPage(self, page):
        #self.page = page
        
    def scan(self, page):
        soup = DOMParser.getDOM(page.content)
        page.content = DOMParser.getParsedContent(page.content)
        done = False
        self.priority = page.priority
        self.disability = page.disability
        self.issues = []
        for feature in self.ruleInterpreter.features:
            if self.isValid(feature.level, feature.rank):
                self.issues.append(feature.rule(soup)) 
                done = True
            else :
                print "Not valid"
                self.issues.append([]) 
        return done
                    
    
    def isValid(self,prio,rank):
        p = (int(self.priority) >= int(prio))
        
        r = False   
        
        for i in self.disability:
            if int(rank)%int(i) == 0:
                r = True
        return p and r
    
    def getEvalResults(self, page):
        evalResults = EvalResults()
        evalResults.setResults(self, self.ruleInterpreter.features, page)
        return evalResults