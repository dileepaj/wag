from wag import app
import datetime

app.config['description'] = 'WAG',
app.config['url'] ='URL to get it at.',
app.config['version'] ='0.1',
app.config['install_requires'] =[''],
app.config['packages'] =[''],
app.config['scripts']  =[],
app.config['name'] ='projectname',
app.config['REMEMBER_TOKEN_DURATION']=datetime.timedelta(days = 30) 
app.config['REMEMBER_COOKIE_DURATION']=datetime.timedelta(days = 7)
app.config['violation_green_limit']=30
app.config['free_violation_limit']=4
app.config['free_project_limit']=1
app.config['default_disability']=[u'2', u'3', u'5']
app.config['default_priority']=3