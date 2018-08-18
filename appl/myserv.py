from flask import Flask,send_file,request,render_template,redirect,url_for,session,flash,jsonify
from dbchecker import auth_user
import os
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def hello():
	if not session.get('logged_in'):
		return redirect(url_for('login_u'))
	else:
		return redirect(url_for('user_feed()'))

@app.route('/login', methods=['GET', 'POST'])
def login_u():
	if request.method == 'POST':
		uname = request.form['uname']
		pwd = request.form['pwd']
		if(uname == 'admin' and pwd == 'pass'):
			session['logged_in'] =True
			session['user'] = uname
			return redirect(url_for('user_feed'))
		else:
			return redirect(url_for('login_u'))
	return render_template('login_user.html')

@app.route('/feed', methods=['GET', 'POST'])
def user_feed():
	return 'HIII!!! I AM USER FEED'

@app.route('/search', methods=['GET', 'POST'])
def search_c():
	return render_template('')
@app.route('api/searching', methods=['GET', 'POST'])
def search_db():
	pass

if __name__=='__main__':
	app.run(debug=True)