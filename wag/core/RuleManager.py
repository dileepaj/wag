from RuleInterpreter import RuleInterpreter
from RuleEvaluator import RuleEvaluator
from Page import Page

class RuleManager(object):
    
    #page = None
    #evaluationResult = None
    
    def __init__(self):
        self.ruleInterpreter = RuleInterpreter()
        self.evaluator = RuleEvaluator(self.ruleInterpreter)
        
        
    def setPage(self,page):
        self.evaluator = RuleEvaluator(self.ruleInterpreter)
        #self.evaluator.setPage(page)
        
    def eval(self, page):
        success = self.evaluator.scan(page)
        if success :
            evaluationResults = self.evaluator.getEvalResults(page)
            print "evaluation successful"
        else:
            print "No violations detected"
            evaluationResults = None
        return evaluationResults
    
    def evalSite(self, site):
        noOfPages = site['urls'].__len__()
        homeUrl = site['urls'][0]
        disabilities = site['disabilities']
        prio = int(site['priority'])
        evaluatedPages = []
        
        for i in range(0, noOfPages):
            page = Page(site['urls'][i], site['contents'][i])
            page.setDisability(disabilities)
            page.setPriority(prio)
            page.evaluationResults = self.eval(page)
            page.setHomeUrl(homeUrl)
            evaluatedPages.append(page)
            
        return evaluatedPages