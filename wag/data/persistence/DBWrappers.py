from DBInterface import DBInterface
from wag import app
from mongokit import Connection, Document, OR
import datetime
from wag.utils.Constants import *

#mongo = PyMongo(app)
if app.config['TESTING']:
    dbname = TEST_DB_NAME
else:
    dbname = DEMO_DB_NAME

class User(Document):
    __collection__ = 'users'
    __database__= dbname
    
    structure = {
        'id' : unicode,
        'email' : unicode,
        'password' : str,
        'type' : str
    }
    
    required_fields = ['id', 'email' , 'password']
    
    use_dot_notation = True
    
        

class Result(Document):
    __collection__ = 'results'
    __database__ = dbname
    
    structure = {
        'site' : unicode,
        'user' : unicode,
        'url' : unicode,
        'priority' : int,
        'disability' : [unicode],
        'violations' : [{
            'id' : int,
            'featureId' : int,
            'element' : str,
            'line' : int,
            'nodeLines' : int,
            'status' : unicode,
        }]
     }
    
    required_fields = ['url']
    default_values = {'priority' : 1}
    
    use_dot_notation = True
    
    def __repr__(self):
        return '<Result %r>' % (self.url)

class PageDB(Document):
    __collection__ = 'pages' 
    __database__ = dbname
    
    structure = {
        'user' : unicode,
        'site' : unicode,
        'url' : unicode,         
        'content' : unicode        
    }
    
    required_fields = ['url']
    
    use_dot_notation = True

class Website(Document):
    __collection__ = 'sites'
    __database__ = dbname
    
    #assuming just a dict for pages
    structure = {
        'user' : unicode,
        'name' : unicode,
        'homeUrl' : basestring,
        'pages' : {
           'urls' : list,
           'contents' : list
        }
    }
    
    #required_fields = ['user']
    
    use_dot_notation = True
    
class PageHistory(Document):
    __collection__ = 'pageHistory'
    __database__ = dbname
    
    #assuming just a dict for pages
    structure = {
         'homeUrl' : basestring,
         'site' : unicode,
         'time' : dict,
         'url' : unicode,
         'content' : unicode,
         'priority' : int,
         'disability' : [unicode],
         'violations' : [{
            'id' : int,
            'featureId' : int,
            'element' : str,
            'line' : int,
            'nodeLines' : int,
            'status' : unicode,
        }],
         'total' : int,
         'resolves' : int,
         'skips' : int,
         'evalNum' : int
    }
    
    #required_fields = ['user']
    default_values = { 'total' : 0 , 'resolves' : 0 , 'skips' : 0}
    use_dot_notation = True
    
class CommunityUser(Document):
    __collection__ = 'communityUser'
    __database__ = 'wag'

    structure = {
        'username' : unicode,
        'useremail' : unicode,
        'userdescription' : unicode,
        'date_creation': datetime.datetime#,
        #'submissions' :[{
         #   'workdescription' : unicode,
         #   'rule' : unicode,
         #   'script' : unicode,
         #   'date_of_submission' : datetime.datetime
        #}]
    }

    required_fields = ['username', 'useremail']
    default_values = {'date_creation':datetime.datetime.utcnow }
    use_dot_notation = True
    
class SiteHistory(Document):
    __collection__ = 'siteHistory'
    __database__ = dbname
    
    structure = {
         'homeUrl' : basestring,
         'name' : unicode,
         'user' : unicode,
         'time' : dict,
         'priority' : int,
         'disability' : [unicode],
         'total' : int,
         'resolved' : int,
         'skips' : int,
         'evalNum' : int
     }
    
    default_values = { 'total' : 0 , 'resolved' : 0 , 'skips' : 0}
    use_dot_notation = True
    
class MongoDBWrapper(DBInterface):
    
    def __init__(self):
        self.connection = self.openConnection()
        self.database = self.connection.wag
    
    def openConnection(self):
        #should be passed in from app.config
        conn = Connection( )
        conn.register([User])
        conn.register([Result])
        conn.register([PageDB])
        conn.register([Website])
        conn.register([PageHistory])
        conn.register([SiteHistory])
        conn.register([CommunityUser])
        
        return conn
    
    def createUser(self, id, email, password, type="Free"):
        newUser = self.connection.User()
        newUser['id'] = id
        newUser['email'] = email
        newUser['password'] = password
        newUser['type'] = type
        
        newUser.save()
        
    def createPage(self, url, content, user, site):
        pageInsert = self.connection.PageDB()
        pageInsert['user'] = user
        pageInsert['site'] = site
        pageInsert['url'] = unicode(url)
        pageInsert['content'] = unicode(content)
              
        pageInsert.save()
        
    def createCommunityUser(self, username, useremail, userdescription, submissionlist):
        new_community_user = self.connection.CommunityUser()
        new_community_user['username'] = username
        new_community_user['useremail'] = useremail
        new_community_user['userdescription'] = userdescription

        #new_community_user['submissions'] = submissionlist if submissionlist is not None else None
        new_community_user.save()
        
    def createResult(self, page, results, user, site=u"None"):
        result = self.connection.Result()
        result['user'] = user
        result['site'] = site
        result['url'] = page.url
        result['priority'] = page.priority
        result['disability'] = page.disability
        result['violations'] = self._getResultsList(results)     
        result.save()
        
    def createWebsite(self, user, name, home, pages):
        site = self.connection.Website()
        site['user'] = user
        site['name'] = name
        site['homeUrl'] = home
        site['pages'] = pages
        site.save()
    
    def createPageHistory(self, page, EvalResult, time, site = u'None'):
        hist = self.connection.PageHistory()
        hist['site'] = site
        hist['homeUrl'] = page.homeUrl
        hist['url'] = page.url
        hist['content'] = unicode(page.content, errors='replace')
        hist['priority'] = page.priority
        hist['disability'] = page.disability
        hist['time'] = time
        hist['violations'] = self._getResultsList(EvalResult.results)
        hist['total'] = EvalResult.total
        hist['resolves'] = EvalResult.resolves
        hist['skips'] = EvalResult.skips
        instances = self.database.pageHistory.find({'url': page.url, 'site' : site}).count()
        hist['evalNum'] = instances + 1
        hist.save()     
        
    def createSiteHistory(self, user, site, time, total):
        hist = self.connection.SiteHistory()
        hist['name'] = site['siteName']
        hist['homeUrl'] = site['urls'][0]
        hist['user'] = user
        hist['time'] = time
        hist['priority'] = int(site['priority'])
        hist['disability'] = site['disabilities']
        hist['total'] = total
        instances = self.database.siteHistory.find({'user': user, 'name' : site['siteName']}).count()
        hist['evalNum'] = instances + 1
        hist.save()
    
    def updatePage(self, url, content, username):
        self.database.pages.update({'url' : url , 'user' : username}, {"$set" : {'content' : content}})
        
    def updateWebSite(self, user, name, pages):
        print "Updating web site"
        self.database.sites.update({'name' : name, 'user': user}, {"$set" : {'pages' : pages}})
        
    def updateResults(self, user, site, page, results):
        self.database.results.update({'user': user, 'site' : site, 'url' : page.url, 'priority' : page.priority, 'disability': page.disability},
                                           {"$set" : {'violations' : self._getResultsList(results)}})
    
    def getUser(self, username):
        user = self.database.users.find_one({'id' : username})
        return user
    
    def changeUserProperty(self, id, property, newVal):
        self.database.users.update({'id' : id}, {"$set" : {property : newVal}})
    
    def getSite(self, name, user):
        site = self.database.sites.find_one({'user' : user, 'name' : name})
        return site
    
    def getSiteTimes(self, name, user):
        histories = self.database.siteHistory.find({'user':user, 'name': name}, fields = ['time'])
        return histories
    
    def _getResultsList(self, results):
        resultList = []
        for r in results:
            result = {
                 'id' : r.id,
                 'featureId' : r.featureId,
                 'element' : r.element,
                 'line' : r.line,
                 'nodeLines' : r.nodeLines,
                 'status' : r.status
            }
            resultList.append(result)
        
        return resultList
    
    def getUserResults(self, user):
        page = self.database.pages.find_one({'user' : user})
        evaluation = self.database.pages.find_one({'url' : page['url']})
        return self._getResultsList(evaluation['violations'])
    
    def getExistingResult(self, url, priority, disability, user):
        existingDoc = self.database.results.find_one({'url' : url, 'user' : user, 'priority' : priority, 'disability' : disability})
        print "finding" + url + "for " + user
        if not existingDoc is None:
           return existingDoc['violations']
        else :
           return None   
    
    def getCriteria(self, url , user):
        existingDoc = self.database.results.find_one({'url' : url, 'user' : user})
        if existingDoc != None:
           return {
                   'priority' : existingDoc['priority'],
                   'disability' : existingDoc['disability']
                   }
        else :
           return None   
    
    def getPage(self, url, user, site):
        page = self.database.pages.find_one({'user' : user, 'url' : url, 'site' : site})
        return page
    
    def getSites(self, user):
        sitelist = self.database.sites.find({'user' : user})
        return sitelist
    
    def changeViolation(self, user, url, id, attrs):
       result = self.database.results.find_one({'url' : url, 'user' : user})
       if result != None:
           violations = result['violations']
           for v in violations:
               if int(v['id']) == int(id):
                   for key,value in attrs.iteritems():
                       v[key] = value
                   break
           
           self.database.results.update({'url' : url, 'user' : user}, {"$set" : {'violations' : violations}})
       else : print "No entry found"
    
    def getSiteHistory(self, name, user):
        result = self.database.siteHistory.find({'user' : user, 'name' : name}, sort = [('evalNum',-1)])
        hists = []
        if not result is None:
            for r in result:
                r.pop(u'_id')
                hists.append(r)
        else:
            hists = None
        return hists
    
    def getPageHistory(self, url, site, evalNum):
        result = self.database.pageHistory.find_one({'site' : site, 'url' : url, 'evalNum':int(evalNum)})
        if not result is None:
            result.pop(u'_id')
        return result
    
    #return page at the point of evaluation
    def getHistoryPage(self, url, site, user, evalNum):
        result = self.database.pageHistory.find_one({'site' : site, 'url': url, 'evalNum' : int(evalNum)})
        if not result is None:
            result.pop(u'_id') 
        else : 
            result = "ERROR : page not found"
        return result
       
    def clearDatabase(self):
       db = self.database
       db.results.remove()
       db.pages.remove()
       db.sites.remove()
       #db.users.remove()     
       db.siteHistory.remove()
       db.pageHistory.remove()