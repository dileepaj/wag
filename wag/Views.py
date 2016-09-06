from Forms import *
from core.Rules import *
from flask import render_template, request, Response, jsonify, redirect, url_for, make_response
from flask_login import login_required, confirm_login, current_user
from flask.helpers import send_from_directory
from wag import app
from wag.AppController import AppController
from wag.core.Page import Page
import json
import urllib2
from functools import wraps
import os
import logging
from werkzeug import secure_filename
import jsonpickle

content = "Nothing to do here"
controller = AppController(app)

############################################ decorators ###########################################
def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def allowXDomain(f):
    """This decorator passes Access-Control-Allow-Origin:<domain>"""
    return add_response_headers({'Access-Control-Allow-Origin': '*'})(f)


############################################ Routing ###########################################
@app.route('/')
def index():
    if not current_user.is_anonymous:
        return render_template('index.html', userid = current_user.id )
    else :
        return render_template('index.html', userid = "Guest" )


@app.route('/home')
def home():
    id = controller.getCurrentUserid()
    confirm_login()
    return render_template('home.html', content = controller.currentPage.content, curUrl = controller.currentPage.url, userid = id, type = "Site")    

@app.route('/dashboard')
@login_required
def dashboard():
    id = controller.getCurrentUserid()
    print "logged in as " + id 
    userType = controller.getCurrentUserType()
    return render_template('dashboard.html', userid = id, userType = userType)


@app.route('/documents')
def documents():
    
    return render_template('documents.html')    

@app.route('/community_home.html', methods=['GET'])
@app.route('/community_tutorial.html', methods=['GET'])
@app.route('/rule_validate.html', methods=['GET'])
@app.route('/rule_upload.html', methods=['GET'])
@app.route('/newProject.html', methods=['GET'])
@app.route('/Dashboard_table.html', methods=['GET'])
@app.route('/History_graph.html', methods=['GET'])
@app.route('/buyPage.html', methods=['GET'])
def partialView():
    return render_template(request.path[1:])


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print "registering user"
        username =  form.username.data
        email = form.email.data
        password = form.password.data
        type = form.userType.data
        userType = 'Paid'
        controller.saveUser(username, email, password, userType)
        controller.loginUser(username, password, False)
	return redirect(url_for('dashboard'))
	
    else :
        print "couldn't register"
        return render_template('register.html', form = form)
		
@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print "login request OK"
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        print remember
        success = controller.loginUser(username, password, remember)
        if success:
            print current_user.id + " Logged in succesfully"
            return redirect(request.args.get("next") or url_for('dashboard'))
        else :
            error = "Wrong Username or Password"
            form.errors['form'] = error
            print error
    return render_template('login.html', form=form)


@app.route('/userUpdateToPaid')
def userUpdateToPaid():
    controller.updateUserType()
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    controller.logoutUser()
    return redirect('')

@app.route('/submitPage', methods = ['POST'])
def submitPage():
    page = Page()
    page.setURL(request.form['url'])
    page.setContent(request.form['content'])
    reqType = request.form['reqType']
    name = request.form['siteName']
    
    if 'disabilities' in request.form:
        val = json.loads(json.dumps(request.form['disabilities']))
        page.setDisabilitiesfromVal(val)
    if 'priority' in request.form:
        page.setPriority(json.loads(json.dumps(request.form['priority'])))
    store = True

    controller.evaluatePage(page)
    
    id = controller.getCurrentUserid()    
    if reqType == 'Page':
       return render_template('home.html', content = unicode(page.content, errors='replace'), siteName = name, curUrl = page.url, userid = id, type = "Page")
    if reqType == 'Site':
       return render_template('home.html', content = unicode(page.content, errors='replace'), siteName = name, curUrl = page.url, userid = id, type = "Site")

@app.route('/resubmitPage', methods=['POST'])
def resubmitPage():
    page = Page()
    page.setURL(request.form['url'])
    page.setContent(request.form['content'])
    reqType = request.form['reqType']
    name = request.form['siteName']
    id = controller.getCurrentUserid()    
    
    if reqType == 'Page':
       return render_template('home.html', content = page.content, siteName = name, curUrl = page.url, userid = id, type = "Page")
    if reqType == 'Site':
       return render_template('home.html', content = page.content, siteName = name, curUrl = page.url, userid = id, type = "Site")


@app.route('/json/submitPage', methods = ['POST'])
def jsonSubmitPage():
    page = Page()
    page.setURL(request.json['url'])
    page.setContent(request.json['content'])
    name = request.json['name']
    
    if 'disabilities' in request.json:
        vals = json.loads(json.dumps(request.json['disabilities']))
        page.setDisability(vals)
    if 'priority' in request.json:
        page.setPriority(json.loads(json.dumps(request.json['priority'])))
    controller.evaluatePage(page)
    
    reqType = request.json['reqType']
    
    id = controller.getCurrentUserid() 
    
    if reqType == 'Page':
       return render_template('home.html', content = unicode(page.content, errors='replace'), siteName = name, curUrl = page.url, userid = id, type = "Page")
    if reqType == 'Site':
       return render_template('home.html', content = unicode(page.content, errors='replace'), siteName = name, curUrl = page.url, userid = id, type = "Site")

@app.route('/wagthis', methods=['GET'])
@login_required
def wagCmd():
    url = request.args.get('url')
    siteName = request.args.get('name')
    type = 'Site'
    #if siteName is not given assume it's a single page evaluation
    if siteName == '' or siteName is None:
        type = 'Page'
    page = controller.getPage(siteName, url)
    if page is None:
        content = ""
    else:
        content = page['content']
    id = controller.getCurrentUserid()
    return render_template('home.html', content = content, siteName = siteName, curUrl = url, userid = id, type = type)

@app.route('/wagthisnew', methods=['GET'])
@login_required
def wagCmdNew():
    url = request.args.get('url')
    siteName = request.args.get('name')
    username = request.args.get('username')
    type = 'Site'
    content = ""
    id = controller.getCurrentUserid()
    return render_template('home.html', content = content, siteName = siteName, curUrl = url, userid = username, type = type)


@app.route('/loadEval', methods=['GET'])
def loadEvaluation():
    page = Page()
    evalNum = request.args.get('evalNum')
    page = controller.getPage(request.args.get('site'), request.args.get('url'), evalNum = evalNum)
    id = controller.getCurrentUserid()
    return render_template('home.html', content = page['content'], siteName=page['site'], curUrl = page['url'], userid = id, evalNum = evalNum, type = "Site")

@app.route('/project', methods=['GET'])
@login_required
def loadProject():
    siteName = request.args.get('site')
    id = controller.getCurrentUserid()
    return render_template('project.html' , name = siteName, userid = id)

@app.route('/reevaluate', methods = ['POST'])
def reevaluate():
    page = Page()
    page.setURL(request.json['url'])
    page.setContent(request.json['content'])
    if 'disabilities' in request.json:
        vals = json.loads(json.dumps(request.json['disabilities']))
        page.setDisability(vals)
   
    if 'priority' in request.json:
        page.setPriority(json.loads(json.dumps(request.json['priority'])))
    
    controller.evaluatePage(page, store=False)
    
    results = controller.getEvalResult(page = page, fromdb = False)
    return jsonify(evalResults = results)

@app.route('/urlSubmit', methods=['POST'])
def urlSubmit():
    url = request.form['url']
    print url
    response = urllib2.urlopen(url)
    print response.read()
    
###### WAG_Community ##########################

#community method declaration here
@app.route('/community', methods = ['GET', 'POST'])
def community():
    if request.method == 'GET':
        return render_template('Community.html')
    elif request.method == 'POST':
        return 'success'
    
#ajax handler implementation
@app.route('/communityupload', methods = ['POST'])
def communityupload():
    if request.method == 'POST':
        json_val = request.form.get('json_val')
        user_name = request.form.get('txt_community_user_name')
        user_email = request.form.get('txt_community_user_email')
        user_work = request.form.get('txt_work_description')
        task_info = request.form.get('task_info')
        file_name = request.files['upload_file']     
        root_path = os.path.dirname(__file__)
        if file_name:
            filename = secure_filename(file_name.filename)
            file_name.save(os.path.join("communityupload", filename))

        controller.createCommunityUser(user_name, user_email, user_work, task_info)
        #return jsonify(result=True)
        return render_template('Community.html')
    
#download WAG Community development bundle                    
@app.route('/downloadwag', methods = ['GET','POST'])
def downloadwag():
    dir = os.path.dirname(__file__)
    filename =os.path.join(dir,"community/WAG_community.zip")
    file = open(filename, 'rb').read() 
    response = make_response(file) 
    response.headers['Content-Type'] = 'application\zip'
    response.headers['Content-Disposition'] = 'attachment; filename=wagcommunity'
    return response

#WAG community new rule test
@app.route('/testnewrule', methods = ['POST'])
def testnewrule():
    print "test new rule"
    rule_eval_result_file = request.files['upload_json']
    test_page_url = request.form['testpageUrl']
    page = Page()
    page.url = test_page_url
    content = urllib2.urlopen(test_page_url).read()
    print content
    page.content = content    
    try:
        if rule_eval_result_file:
            print "file exists"           
            jsonvalue = rule_eval_result_file.read() 
            rule_eval_result_file.close()           
            #print jsonvalue
            if jsonvalue:                
                try:
                    json_obj = jsonpickle.decode(jsonvalue)                   
                    return render_template('ResultsView.html', content = unicode(page.content, errors='replace'), curUrl = test_page_url, type = "Page", json_object = jsonvalue)                 
                except:
                    print "invalid json"
        else:
            print "please upload a file" 
    except:
        print "Error in reading input json file"    
    return 'success'
    
#for testing
@app.route('/ALSI')
@allowXDomain
def test():
    return render_template('ALSI.html')

@app.route('/ALSI2')
@allowXDomain
def test2():
    return render_template('ALSI2.html')

@app.route('/ALSI3')
@allowXDomain
def test3():
    return render_template('ALSI3.html')

@app.route('/ALSI4')
@allowXDomain
def test4():
    return render_template('ALSI4.html')

@app.route('/ALSI_good')
@allowXDomain
def test_good():
    return render_template('ALSI_good.html')

#to serve the knowledgeBase
@app.route('/knowledgeBase.xml')
def static_from_route():
    return send_from_directory("./static", request.path[1:])

@app.route('/filter', methods = ['POST'])
def filter():
    return jsonify(disability = controller.currentPage.getDisability(),
                         priority = controller.currentPage.level)

###############################- Json calls -##########################################

#Show the results page for community developed rule
@app.route('/resultsTestPage', methods = ['POST'])
def resultsTestPage():
    pageUrl = request.json['url']
    json_val = request.json['json_value']
    if json_val is not None:       
        results = jsonpickle.decode(json_val)
        print results
    else :
        results = "No Results Found"
    return jsonify(evalResults = results)
    
@app.route('/resultsPage', methods = ['POST'])
def resultsPage():
    results = None
    pageUrl = request.json['url']
    results = controller.getEvalResult(page = controller.currentPage)
    
    return jsonify(evalResults = results)

@app.route('/resultsSite', methods = ['POST'])
def resultsSite():
    results = None
    homeUrl = request.json['url']
    siteName = request.json['siteName']
    evalNum = request.json['evalNum']
    username = request.json['username']
    if not current_user.is_anonymous:
        username = controller.getCurrentUserid()
        if evalNum == u'None' or evalNum == '': 
           print "Get the latest evaluation"
           results = controller.getSiteResults(username, url = homeUrl, name = siteName)
        else:
           print "evalNum is found"
           results = controller.getSiteResults(username, url = homeUrl, name = siteName, evalNum = evalNum)
    else :
        print "Jenkins call"
        results = controller.getSiteResults(username, url = homeUrl, name = siteName)

    return jsonify(siteResults = results)

@app.route('/progress', methods = ['POST'])
def progress():
    return jsonify(progress = controller.getProgress(controller.currentPage))

@app.route('/skip', methods = ['POST'])
def skip():
    controller.skip(json.dumps(request.json['url']), json.dumps(request.json['id']))  
    return jsonify(response = "None")

@app.route('/pageCollection', methods = ['POST'])
def pages():
    username = request.json['user']
    controller.evaluateSite(username, site = request.json)
    return jsonify(response = "None")
    
@app.route('/projectList', methods = ['POST'])
def projectList():
    print "Project List"
    sitelist = controller.getCurrentUserProjects()
    if sitelist != None :
        return jsonify(siteList = sitelist)
    else :
        return jsonify(error = "Projects not found for user")

@app.route('/pagesList', methods = ['POST'])
def pagesList():
    #home = request.json['homeUrl']
    name = request.json['name']
    pageslist = controller.getPagesofProject(name, controller.getCurrentUserid())
    if pageslist != None :
        return jsonify(pagesList = pageslist)
    else :
        return jsonify(error = "Pages not found for project")

@app.route('/projectHistory', methods=['POST'])
def projectHistory():
    homeName = request.json['home']
    projectHistory = controller.getProjectHistory(homeName)
    if projectHistory != None :
        return jsonify(result = projectHistory)
    else :
        return jsonify(error = "History not found for project")


###################################- WAG Jenkins Calls -###############################

@app.route('/calcScore', methods = ['POST'])
def calcScore():
    site = request.args.get('name')
    user = request.args.get('user')
    totalDefects, evalNum = controller.getDefectsCount(user, site)
    pageCount = controller.getPagesofProject(site, user).__len__()
    score = 100-(totalDefects/pageCount)
    
    finalScore=str(score)
    print finalScore
    return finalScore

@app.route('/evalNum', methods = ['POST'])
def latestEvalNum():
    print "Querying eval Num"
    site = request.args.get('name')
    user = request.args.get('user')
    totalDefects, evalNum = controller.getDefectsCount(user, site)
    
    print evalNum
    
    return str(evalNum)

@app.route('/jenkinsPagesList', methods = ['POST'])
def jenkinspagesList():
    #home = request.json['homeUrl']
    site = request.args.get('name')
    user = request.args.get('user')
    pageslist = controller.getPagesofProject(site, user)
    if pageslist != None :
        return jsonify(pagesList = pageslist)
    else :
        return jsonify(error = "Pages not found for project")
    

###############################- Error pages -##########################################
@app.errorhandler(401)
def page_not_found(e):
    return Response('Login failed')

@app.errorhandler(403)
def unauthorized_access(e):
    return Response('Unauthorized')

################################- Images -########################################
@app.route('/img/<path:imgName>')
def sendImage(imgName):
    return send_from_directory("./static", request.path[1:])
	
@app.route('/reports/<path:projectName>')
def sendPdf(projectName):
    return send_from_directory("./static", request.path[1:])
	




###################################################################################################
IPN_URLSTRING = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
IPN_VERIFY_EXTRA_PARAMS = (('cmd', '_notify-validate'),)
from itertools import chain

def ordered_storage(f):
    import werkzeug.datastructures
    import flask
    def decorator(*args, **kwargs):
        flask.request.parameter_storage_class = werkzeug.datastructures.ImmutableOrderedMultiDict
        return f(*args, **kwargs)
    return decorator

@app.route('/paypal/', methods=['POST', 'GET'])
@ordered_storage
def paypal_webhook():
    #probably should have a sanity check here on the size of the form data to guard against DoS attacks
    verify_args = chain(request.form.iteritems(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value) for param, value in verify_args))
    #req = Request(verify_string)
    response = urlopen(IPN_URLSTRING, data=verify_string)
    status = response.read()
    print status
    if status == 'VERIFIED':
        print "PayPal transaction was verified successfully."
        # Do something with the verified transaction details.
        payer_email =  request.form.get('payer_email')
        print "Pulled {email} from transaction".format(email=payer_email)
    else:
         print 'Paypal IPN string {arg} did not validate'.format(arg=verify_string)

    return jsonify({'status':'complete'})


