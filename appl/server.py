from flask import Flask,send_file,request,render_template,redirect,url_for,session,flash,jsonify
from dbchecker import auth_user
from dbconnector import connection
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
	return render_template("user_dashboard.html")
	#return 'Hello World'
	'''
	if not session.get('logged_in'):
		if(request.method == 'GET' or request.method == 'POST'):
			#return redirect(url_for('login_user'))
			pass
		#return render_template("login_user.html")
	else:
		return redirect(url_for('show_feed'))
'''
	'''
	if not session.get('logged_in'):
		return render_template('login_user.html')
    else:
    	return redirect(url_for('show_feed'))'''
'''
@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
			session['logged_in'] = True
			session['user'] = request.form['username']
			return redirect(url_for('show_feed'))
    return render_template('login_user.html', error=error)'''
@app.route('/login', methods=['GET', 'POST'])
def login_user():
	error = None
	if request.method == 'POST' or request.method == 'GET':
		if request.form['uname'] != 'admin' or request.form['pwd'] != 'pass':
			error = 'Invalid Credentials. Try again.'
		else:
			session['logged_in'] = True
			session['user'] = request.form['uname']
			return redirect(url_for('show_feed'))
	return render_template('login_user.html', error=error)

@app.route('/home')
def show_feed():
	if not session.get('logged_in'):
		return redirect(url_for('login_user'))
	else:
		return "I'm newsfeed! HAHAHA"

@app.route('/get_complaints')
def get_complaints():
	'''info = {
       "ip" : "127.0.0.1",
       "hostname" : "everest",
       "description" : "Main server",
       "load" : [ 3.21, 7, 14 ]
    }
	return jsonify(info)'''
	

	c,conn=connection()
	rows = c.execute("select * from COMPLAINTS ORDER BY c_time_of_lodging DESC;");
	if rows > 0:
		results=c.fetchall()
		arr=[]
		for i in range(len(results)):
			arr.append(results[i])
			print("Hello")
		print("Out of loop")
	return jsonify(arr)


if __name__=='__main__':
	app.run(debug=True)