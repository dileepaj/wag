from DBInterface import DBInterface
from DBWrappers import *
import json
from wag.core.Page import Page
from wag import app
from wag.utils.DOMParser import getParsedContent

class Persistence(object):
    
    def __init__(self):
        self.db = MongoDBWrapper()
    
    def clearDB(self):
        self.db.clearDatabase();
        
    def storeEvaluation(self, page, user, site):
        print user
        self.db.createResult(page, page.evaluationResults.results, user, site)
    
    def storePageHistory(self, page , time, site):
        self.db.createPageHistory(page, page.evaluationResults, time, site)
        
    def storeSiteHistory(self, user, site, time, totErr):
        self.db.createSiteHistory(user, site, time, totErr)
        
    def getEvaluation(self, page, user):
        return self.db.getExistingResult(page.url, page.priority, page.disability, user)
    
    def createCommunityUser(self, username, useremail, userdescription, submissionlist):
        return self.db.createCommunityUser(username, useremail, userdescription, submissionlist)
    
    def getSiteResults(self, user, name, evalNum):
        site = self.db.getSite(name, user)
        resultCollection = []
        if not site is None:
            i = 0
            for pageUrl in site['pages']['urls']:
                if evalNum > 0 : 
                    oldPage = self.db.getHistoryPage(pageUrl, name, user, evalNum)
                    site['pages']['contents'][i] = oldPage['content']
                    i = i + 1
                    evalResult = oldPage['violations']    
                else :
                    print "getting the latest eval results"
                    oldPage = self.db.getHistoryPage(pageUrl, name, user, 1)
                    evalResult = self.db.getExistingResult(pageUrl, int(oldPage['priority']), oldPage['disability'], user)
                    
                resultCollection.append(evalResult)
        
        #because mongodb adds and _id 
            site.pop(u'_id') 
            return {
                    'site' : site,
                    'evalResults' : resultCollection
                     }
        else :
            error = "ERROR:" + name + " not found"
            print error
            return error
    
    def updateEvaluation(self, page, results, user, site):
        self.db.updateResults(user, site,  page, results)
    
    def insertPage(self, page, user, site=u"None", store = True):
        exPage = self.db.getPage(page.url, user, site)
        if exPage:
            if store:
                self.db.updatePage(page.url, page.content, user)
            criteria = self.db.getCriteria(page.url, user)
            if page.disability is None:
                if criteria:
                    page.disability = criteria['disability']
                else :
                    page.disability = app.config['default_disability']
            if page.priority is None:
                if criteria:
                    page.priority = criteria['priority']
                else :
                    page.priority =  app.config['default_priority']
        else:
            print "Insert New Page"
            self.db.createPage(page.url, page.content, user, site)
        return page
        
    def getEvalCriteria(self, url, user):
        return self.db.getCriteria(url, user)
            
    def insertUser(self, user):
        self.db.createUser(user.id.lower(), user.email, user.password, user.type)
        
    def saveSite(self, user, site):
        oldsite = self.db.getSite(site['siteName'], user)
        
        #changing contents as parsed from the parser
        #because then line number references are accurate
        parsedContents = []
        for c in site['contents']:
            parsedContents.append(getParsedContent(c))
        
        if oldsite is None:
            print "Completely new Site"
            pages = {
                 'urls' : site['urls'],
                 'contents' : parsedContents
            }
            self.db.createWebsite(user, site['siteName'], site['urls'][0], pages)
        else:
            print "Updating existing site"
            pages = {
                 'urls' : site['urls'],
                 'contents' : parsedContents
            }
            self.db.updateWebSite(user, site['siteName'], pages)
        
        #save pages in site in the pages collection    
        noOfPages = site['urls'].__len__()
        for i in range(0,noOfPages):
            page = Page(site['urls'][i], site['contents'][i])
            page.setDisability(site['disabilities'])
            page.setPriority(site['priority'])
            self.insertPage(page, user, site['siteName'])
    
    def getPage(self, user, siteName, url, evalNum):
        if evalNum > 0 :
            neededPage = self.db.getPageHistory(url, siteName, evalNum)
                
            if neededPage is None:
                print "ERROR: Evaluation not found in history"
            
            return neededPage    
        
        else :
            return self.db.getPage(url, user, siteName)
                
    def getSite(self, name, user):
        return self.db.getSite(name, user)
    
    def getSiteHistoryTimes(self, name, user):
        return self.db.getSiteTimes(name, user)
    
    #returns the whole list of history elements for the named site
    def getSiteHistory(self, user, name):
        return self.db.getSiteHistory(name, user)
    
    def updateUser(self, id, property, newVal):
        self.db.changeUserProperty(id, property, newVal)
    
    def getUser(self, username):
        return self.db.getUser(username)
    
    def changeViolation(self, user, url, id, attrs):
        index = id.strip("\"")
        self.db.changeViolation(user, url, index,  attrs)
    
    def getSites(self, user):
        sites = self.db.getSites(user)
        siteArray = []    
        if sites != None :
            for s in sites:
                s.pop(u'_id')
                siteArray.append(s) 
            
            return siteArray
        else  :
            print "ERROR : The current user has no projects"
            return None
        
        
        
   