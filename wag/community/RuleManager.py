from bs4 import BeautifulSoup   
from Rules import *
from RuleEvalResult import *
from Features import Feature
import jsonpickle
import urllib2
import sys, re

 
class RuleManager: 
    results = []
    features = []
    rules = Rules() 
    total = 0   
    
    def __init__(self):
        self.featuresoup = BeautifulSoup(open("web_accessibility_spec.xml"), "xml")
        self.features = self.makeFeatureCollection()         
    
    def makeFeatureCollection (self):
        for i in self.featuresoup.findAll("FEATURE"):
            self.features.append(Feature(i.TITLE.get_text(),i.DISABILITY.get_text(),i.DISABILITY['rank'],i.PRIORITY,i.PRIORITY['level'],i.ERROR.get_text(),i.DESCRIPTION.get_text(),i.SOLUTION.get_text(),self.rules.getRule(i['id']))) 
        return self.features   
    
    def setResults(self):
        self.results = []
        items = self.issues
        if items != None:
            i = self.total
            itemNo = 0
                        
            for k in items:
                if k != None:
                    if len(k) > 0:
                       for j in k:
                            i = i + 1
                            elem = self.getStrfromDOM(j)
                            result = RuleEvalResult(i, itemNo, elem)
                            result.ftrInfo = self.getFeatureDict(itemNo)
                            result.line = self.getLine(j, self.content)    
                            self.results.append(result)
                
                itemNo = itemNo + 1
        else:
            print "No Issues found"                     
        self.total = i
        return jsonpickle.encode(self.results)
    
    def getFeatureDict(self, index):
        ftrDict = {'title' : self.features[index].title,
                    'disability' : self.features[index].disability,
                    'error' : self.features[index].error,
                    'description' : self.features[index].description,
                    'solution' : self.features[index].solution,
                    'priority' : self.features[index].level,
                    'rank' : self.features[index].rank
                    }
        return ftrDict
    
    def createResultFile(self, evalResults):
        text_file = open("RuleEvalResults.txt", "w")
        text_file.write(evalResults)
        text_file.close()
        
    def getStrfromDOM(self, soupNode):
        soupString = str(soupNode)
        normalString = soupString.replace("\\\"", "").replace("\'", "\"")
        return normalString
        
    def scan(self, test_page_url):        
        self.content = urllib2.urlopen(test_page_url).read()
        self.soup = BeautifulSoup(self.content)     
        done = False       
        self.issues = []
        for feature in self.features:          
            self.issues.append(feature.rule(self.soup)) 
            done = True         
        return done
    
    def getLine(self, soupNode, Content):
        srsCode = str(self.soup)  
        nodeString = str(soupNode)
        #nodeString = nodeString.replace("\"", "\\\"")
        index = srsCode.find(nodeString)
        if( index != -1 ):
            untilSlice = srsCode[0:index]
            line = untilSlice.count('\n')
            #because bs4 removes whitespace lines.
            extraLines = untilSlice.count('\n\n')
            print extraLines
        return line - extraLines
        
def main():
    
    rulemanager = RuleManager()
    url_val = sys.argv[1]
    is_url = x = re.match('^(http(?:s)?\:\/\/[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,6}(?:\/?|(?:\/[\w\-]+)*)(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+)*)$', url_val)

    if url_val is not None:  	
        rulemanager.scan(url_val)
        print url_val    
        evalResults = rulemanager.setResults() 
        rulemanager.createResultFile(evalResults)
        print "Successful...."
    else:
	    print "Invalid URL, please enter a correct url"
    
if __name__ =='__main__':main()


        
