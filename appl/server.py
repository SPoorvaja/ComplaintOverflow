from flask import Flask,send_file,request,render_template,redirect,url_for,session,flash,jsonify
from dbchecker import auth_user
app = Flask(__name__)


@app.route('/')
def hello_world():
	#return 'Hello World'
	if not session.get('logged_in'):
		return render_template("login_user.html")
	else:
		return "I'm your user feed."
	'''
	if not session.get('logged_in'):
		return render_template('login_user.html')
    else:
    	return redirect(url_for('show_feed'))'''

'''@app.route('/login')
def login_user():
	if(request.method == 'POST'):
		uname = request.form['uname']
		passwd = request.form['pwd']
		if(auth_user(uname,pwd) == True):
			session['logged_in'] = True
			session['user'] = uname
			return redirect(url_for('hello_world'))
	return render_template('login_user.html')'''

@app.route('/home')
def show_feed():
	if not session.get('logged_in'):
		return redirect(url_for('login_user'))
	else:
		return "I'm newsfeed! HAHAHA"


if __name__=='__main__':
	app.run(debug=True)