from Page import Page
from wag.utils.DOMParser import *

def enum(**enums):
    return type('Enum', () , enums)

States = enum(UNRESOLVED = u'Unresolved' , 
              IGNORE = u'Skipped',
              RESOLVED = u'Solved')

class EvalResults(object):
    results = []
    total = 0
    resolves = 0
    skips = 0
    
    def setResults(self, scanner, features, page):
        self.results = []
        items = scanner.issues
        if items != None:
            i = self.total
            itemNo = 0
            
            for k in items:
                if k != None:
                    if len(k) > 0:
                       for j in k:
                            i = i + 1
                            elem = getStrfromDOM(j)
                            result = RuleEvalResult(i, itemNo, elem, page)
                            result.ftrInfo = scanner.ruleInterpreter.getFeatureDict(itemNo)
                            result.line = getLine(j, page.content)    
                            self.results.append(result)
                itemNo = itemNo + 1
        else:
            print "No Issues found" 
                                
        self.total = i
        
    def modifyResults(self, oldResults, page, ruleInterpreter):
        modifiedResults = []
        for olres in oldResults:
            exists = False
            for res in self.results:
                if not res in modifiedResults:
                    modifiedResults.append(res)
                if olres['featureId'] == res.featureId:
                    if (olres['element'] == res.element): 
                        exists = True
                        res.id = olres['id']
                        break
                    else :
                        #if the element has been changed, 
                        #assume the violation is same if the line number is same
                        if olres['line'] == res.line:
                            exists = True 
            if not exists:
                olres['status'] = States.RESOLVED
                #Eventhough element is stored as str Mongokit returns it as unicode
                olres['element'] = convertToStr(olres['element'])            
                solvedRes = RuleEvalResult(olres['id'], olres['featureId'], olres['element'], page)
                solvedRes.ftrInfo = ruleInterpreter.getFeatureDict(olres['featureId'])
                solvedRes.status = States.RESOLVED
                solvedRes.line = olres['line']
                #self.results.append(solvedRes)
                modifiedResults.append(solvedRes)
                self.total = self.total + 1
                self.resolves = self.resolves + 1
        
        self.results = modifiedResults
        return self.results
        
class RuleEvalResult(object):
    
    id = 0;
    element = None
    line = 0;
    nodeLines = 0;
    status = ''
    page = None
    error = ''
    
    def __init__(self, id, type, elem, page):
        self.page = page
        self.id = id
        self.featureId = type
        self.element = elem
        self.nodeLines = getNodeLineCount(elem)
        self.status = States.UNRESOLVED
        self.ftrInfo = None
    
    def resetLine(self):
        self.line = getLine(self.element, self.page.content)
        
   