from wag import app
import setup
print 'Server running'
#app.run(host='127.0.0.1', debug=True)
app.run(host='0.0.0.0', port=int('5000'), debug=False)