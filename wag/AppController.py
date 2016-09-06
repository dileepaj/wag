from wag import app
from core.RuleInterpreter import RuleInterpreter
from core.RuleEvaluator import RuleEvaluator
from core.RuleManager import RuleManager
from flask_login import LoginManager, login_user, current_user, logout_user
from core.Page import Page
from data.persistence.Persistence import *
from data.userdata.User import *
import datetime
from wag.utils.timeFormat import *
from wag.utils.reporting import *
from wag.utils.DOMParser import convertToStr
from flask_login import logout_user


class AppController(object):
    #page = None
    #evaluationResult = None

    def __init__(self, app):
        self.ruleManager = RuleManager()
        self.persist = Persistence()
        #self.persist.clearDB()
        self.users = []
        #for anon users
        self.currentPage = None

    def setPage(self, page, site, store):
        if not current_user.is_anonymous:
            page = self.persist.insertPage(page, current_user.id, site, store)
        if page.disability is None:
            page.disability = self.currentPage.disability
        if page.priority is None:
            page.priority = self.currentPage.priority
        self.currentPage = page

        return page

    def getPage(self, site, url, evalNum=0):
        page = self.persist.getPage(self.getCurrentUserid(), site, url, evalNum)
        return page

    def saveUser(self, username, email, password, type):
        user = User(username, email, password, type)
        user.save()
        
    def updateUserType(self):
        id = self.getCurrentUserid()
        self.persist.updateUser(id, "type", 'Paid')
        

    def getCurrentUserid(self):
        if current_user.is_anonymous:
            id = u"Guest"
        else:
            id = current_user.id
        return id

    def loginUser(self, username, password, remember):
        user = User.get(username.lower())
        if user and hash_pass(password) == user.password:
            login_user(user, remember)
            self.users.append(user)
            return True
        else:
            return False

    def logoutUser(self):
        logout_user()

    def evaluatePage(self, page, site=u'Default', store=True):
        page = self.setPage(page, site, store)
        #get page from db if existing
        page.evaluationResults = self.ruleManager.eval(page)
        #no existing results for anon users
        existingResults = None
        if not current_user.is_anonymous:
            existingResults = self.persist.getEvaluation(page, self.getCurrentUserid())
            if not existingResults is None:
                existingResults = page.evaluationResults.modifyResults(existingResults, page,
                                                                       self.ruleManager.ruleInterpreter)

        if store:
            print "saving evaluation"
            evalTime = serializeDatetime(datetime.datetime.now())
            self.storeEvaluation(page, evalTime, site, existingResults)

    def skip(self, url, id):
        self.persist.changeViolation(url, id, {'status': 'skip'})

    def storeEvaluation(self, page, evalTime, sitename, existingResults):
        if not existingResults is None:
            print "Updating existing evaluation"
            self.persist.updateEvaluation(page, existingResults, self.getCurrentUserid(), sitename)
        else:
            print "store New evaluation"
            self.persist.storeEvaluation(page, self.getCurrentUserid(), sitename)

        #keep history only if user in not anon    
        if not current_user.is_anonymous:
            self.persist.storePageHistory(page, evalTime, sitename)

    def getEvalResult(self, page=None, fromdb=False, url=" "):
        minResults = []
        #modify to explicitly retrieve from db
        if fromdb:
            print "getting results from db for " + url
            pageResults = self.persist.getEvaluation(page, self.getCurrentUserid())
            if not pageResults is None:
                for r in pageResults:
                    r['ftrInfo'] = self.ruleManager.ruleInterpreter.getFeatureDict(r['featureId'])
                minResults = pageResults
            else:
                print "ERROR : data not in db"
        else:
            print "getting results from last submit"
            for r in page.evaluationResults.results:
                minResults.append({'id': r.id,
                                   'line': r.line,
                                   'nodeLines': r.nodeLines,
                                   'status': r.status,
                                   'element': r.element,
                                   'ftrInfo': r.ftrInfo})

        #Only 4 violations will be shown for free users
        userType = self.getCurrentUserType()
        if userType == 'Free':
            while minResults.__len__() > app.config['free_violation_limit']:
                minResults.pop()

        return minResults
    
    def createCommunityUser(self, username, useremail, userdescription, submissionlist):
        saved_state = self.persist.createCommunityUser(username, useremail, userdescription, submissionlist)

    def getCurrentUserType(self, user=None):
        #if user is not provided, then get the current logged in user
        if user is None:
            user = self.getCurrentUserid()
        if current_user.is_anonymous:
            return "Guest"
        userType = self.persist.getUser(user)['type']
        return userType

    def getSiteResults(self, user, url, name, evalNum=0):
        siteResults = self.persist.getSiteResults(user, name, evalNum)
        if siteResults is None:
            print "ERROR : no site found in the db"
        resultCollection = siteResults['evalResults']
        size = resultCollection.__len__()
        for i in range(0, size):
            #pageResults holds the evalresults of the ith page in the pages collection
            pageResults = resultCollection[i]
            for r in pageResults:
                ftrInfo = self.ruleManager.ruleInterpreter.getFeatureDict(r['featureId'])
                r['ftrInfo'] = ftrInfo
        return siteResults

    def getProgress(self, page):
        return {'total': page.evaluationResults.total,
                'skips': page.evaluationResults.skips,
                'resolves': page.evaluationResults.resolves}

    #Store the given pages collection in db    
    def storeSite(self, user, site):
        if not current_user.is_anonymous:
            if self.getCurrentUserType(user) == 'Free':
                print "free user"
                sites = self.persist.getSites(user)
                if sites.__len__() > 1:
                    print "Free User Not allowed to create this site"
                    return False
                else:
                    self.persist.saveSite(user, site)
                    return True
            else:
                print "Paid user"
                self.persist.saveSite(user, site)
                return True

    def restoreSiteSettings(self, site):
        #currently no way to change eval criteria in resubmit, so getting one from history is enough
        oldSites = self.persist.getSiteHistory(self.getCurrentUserid(), site['siteName'])
        if oldSites.__len__() != 0:
            oldSite = oldSites[0]
            if not 'disabilities' in site:
                site['disabilities'] = oldSite['disability']

            if not 'priority' in site:
                site['priority'] = oldSite['priority']

        else:
            print "Setting default criteria"
            if not 'disabilities' in site:
                site['disabilities'] = app.config['default_disability']
            if not 'priority' in site:
                site['priority'] = app.config['default_priority']

        return site
        #evaluate the site

    def evaluateSite(self, user = None, site = None):
        site = self.restoreSiteSettings(site)
        
        #if user not provided get the current logged in user
        if user is None:
            user = self.getCurrentUserid()
            
        if site is None:
            print "SERVER ERROR, insufficient data"
            return "ERROR"
        
        evalTime = datetime.datetime.now()
        serializedTime = serializeDatetime(evalTime)

        evaluatedPages = self.ruleManager.evalSite(site)

        noOfPages = evaluatedPages.__len__()
        totalErrors = 0
        for page in evaluatedPages:
            existingResults = self.persist.getEvaluation(page, user)
            if not existingResults is None:
                existingResults = page.evaluationResults.modifyResults(existingResults, page,
                                                                       self.ruleManager.ruleInterpreter)

            self.storeEvaluation(page, serializedTime, site['siteName'], existingResults)
            totalErrors = totalErrors + page.evaluationResults.total - page.evaluationResults.resolves
        if not current_user.is_anonymous:
            self.persist.storeSiteHistory(user, site, serializedTime, totalErrors)
        
        generateReport(site['siteName'], evaluatedPages)
        
        self.storeSite(user,site)

        print "SITE EVAL FINISHED"

    #get progress method for project

    def getCurrentUserProjects(self):
        userSites = self.persist.getSites(current_user.id)
        for site in userSites:
            sitetimes = self.persist.getSiteHistoryTimes(site['name'], current_user.id)
            siteHist = self.persist.getSiteHistory(self.getCurrentUserid(), site['name'])
            if siteHist.__len__() > 0:
                latestHist = None
                dtmax = datetime.datetime.min
                for siteinst in siteHist:
                    dt = deserializeDatetime(siteinst['time'])
                    if dt > dtmax:
                        dtmax = dt
                        latestHist = siteinst

                violCount = latestHist['total']
                site['violationCount'] = violCount

                if violCount > app.config['violation_green_limit']:
                    site['status'] = "uncool"
                else:
                    site['status'] = "cool"

            else:
                site['violationCount'] = "ERROR"
                site['status'] = "---"
            datetimes = []
            if sitetimes.count() > 0:
                for time in sitetimes:
                    dt = datetime.datetime(time['time'][u'year'], time['time']['month'], time['time']['day'],
                                           time['time']['hour'], time['time']['minute'])
                    datetimes.append(dt)

                datetimes.sort()
                site['SubmitTime'] = formatDatetime(datetimes[0])
                site['LastEvalTime'] = formatDatetime(datetimes[datetimes.__len__() - 1])
                #get the created, last eval dates
                #add it to each sites entry
            else:
                site['SubmitTime'] = "---"
                site['LastEvalTime'] = "---"

        return userSites
    
    def getDefectsCount(self, username, siteName):
        userSites = self.persist.getSites(username)
        violCount = 0
        evalNum = 0
        for site in userSites:
            if site['name'] != siteName:
                continue
            sitetimes = self.persist.getSiteHistoryTimes(site['name'], username)
            siteHist = self.persist.getSiteHistory(username, site['name'])
            if siteHist.__len__() > 0:
                latestHist = None
                dtmax = datetime.datetime.min
                for siteinst in siteHist:
                    dt = deserializeDatetime(siteinst['time'])
                    if dt > dtmax:
                        dtmax = dt
                        latestHist = siteinst
                evalNum = latestHist['evalNum']            
                violCount = latestHist['total']
                break

        return violCount, evalNum
  
    def getPagesofProject(self, sitename, user= "Anonymous"):
        siteResults = self.persist.getSiteResults(user, sitename, 0)
        if siteResults is None:
            print "ERROR : no site found in the db"
        else:
            return siteResults['site']['pages']['urls']

    def getProjectHistory(self, name):
        siteHist = self.persist.getSiteHistory(current_user.id, name)
        if siteHist is None:
            print "ERROR : no site found in the db"
        else:

            for inst in siteHist:
                allViolations = []
                evalNum = inst['evalNum']
                siteUrls = self.getPagesofProject(inst['name'], current_user.id)
                for url in siteUrls:
                    page = self.getPage(inst['name'], url, evalNum)
                    if not page is None:
                        allViolations.extend(page['violations'])
                self.getViolationMap(allViolations)
                inst['allViolations'] = allViolations
            return siteHist

    def getViolationMap(self, violations):
        ri = RuleInterpreter()

        for v in violations:
            ftrInfo = ri.getFeatureDict(v['featureId'])
            v['title'] = ftrInfo['title']
            v['priority'] = ftrInfo['priority']
            v['rank'] = ftrInfo['rank']
