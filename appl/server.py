from flask import Flask,send_file,request,render_template,redirect,url_for,session,flash,jsonify
from dbchecker import auth_user, search_db
from dbconnector import connection
from datetime import datetime
import os
import string
import random
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if session.get('logged_in'):
		return render_template("user_dashboard.html")
	else:
		return redirect(url_for('login_u'))
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
def login_u():
	if request.method == 'POST':
		uname = request.form['uname']
		pwd = request.form['pwd']
		if(uname == 'admin' and pwd == 'pass'):
			session['logged_in'] =True
			session['user'] = uname
			return redirect(url_for('hello_world'))
		else:
			return redirect(url_for('login_u'))
	return render_template('login_user.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def login_admin():
	if request.method == 'POST':
		uname = request.form['uname']
		pwd = request.form['pwd']
		if(uname == 'admin' and pwd == 'password'):
			session['logged_in'] =True
			session['user'] = uname
			return redirect(url_for('admin_home'))
		else:
			return redirect(url_for('login_admin'))
	return render_template('login_admin.html')

	'''if request.method == 'POST':
		uname = request.form['admin']
		paswd = request.form['pwd']
		if(uname == 'admin' and paswd == 'password'):
			session['logged_in'] = True
			session['user'] = uname
			session['admin'] = True
			return redirect(url_for('admin_home'))
		else:
			return redirect(url_for('login_admin'))
	return render_template('login_admin.html')'''

@app.route('/adminhome')
def admin_home():
	render_template('admin_home.html')

@app.route('/home')
def show_feed():
	if not session.get('logged_in'):
		return redirect(url_for('login_user'))
	else:
		return "I'm newsfeed! HAHAHA"

@app.route('/get_complaints')
def get_complaints():
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

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
	print(request.args['HIII']);
	return redirect(url_for('hello_world'))

@app.route('/api/search', methods=['GET', 'POST'])
def search_q():
	keyword = request.args.get('q')
	if keyword is not None:
		lis = search_db(keyword)
	if lis is not None:
		return jsonify(lis)

@app.route('/logout', methods=['GET', 'POST'])
def log_out():
	session['logged_in'] = False
	session['user'] = None
	return redirect(url_for('login_u'))

@app.route('/lodge_complaint_page', methods=['GET', 'POST'])
def lodge_complaint_page():
	return render_template('lodge_complaint.html')


@app.route('/reask', methods=['GET', 'POST'])
def reask():
	c,conn=connection()
	uid= session['user']
	cid = request.args['c']
	print("PID = ")
	print(uid)
	print("CID =")
	print(cid)
	rowcount1 = c.execute("select * from PUBLIC_COMPLAINTS where p_uid_f='" + uid  + "' and c_id_uf='"+cid+"';");
	if rowcount1>0:
		return redirect(url_for('hello_world'))
	rows = c.execute("insert into PUBLIC_COMPLAINTS values('"+str(uid)+"','"+str(cid)+"','"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"');");
	row1 = c.execute("update COMPLAINTS set c_time_of_lodging = '"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"' where c_id = "+cid+";")
	conn.commit()
	c.close()
	return redirect(url_for('hello_world'))

@app.route('/get_my_complaints')
def get_my_complaints():
	c,conn = connection()
	uid = session['user'];
	rows = c.execute("select c.c_id,c.c_dept,c.c_subject,c.c_text,pc.time_of_lodging,c.c_status, (select count(*) from PUBLIC_COMPLAINTS pc2 where pc2.c_id_uf = pc.c_id_uf) as reasks from COMPLAINTS c, PUBLIC_COMPLAINTS pc where c.c_id=pc.c_id_uf and pc.p_uid_f = '" + uid + "';")
	res=[]
	if rows > 0:
		res = c.fetchall()
	return jsonify(res)

@app.route('/lodge_complaint', methods=['GET', 'POST'])
def lodge_complaint():
	c,conn=connection()
	uid= session['user']
	cid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	cdept = request.args['c_dept']
	'''csubject = request.args['c_subject']
	cbody = request.args['c_body']

	print("PID = ")
	print(uid)
	print("CiD = ")
	print(cid)
	print("c_dept = ")
	print(cdept)
	print("Csubject = ")
	print(csubject)
	print("Cbody = ")
	print(cbody)
	rowcount1 = c.execute("insert into COMPLAINTS values('"+cid+"','"+str(cdept)+"', '"+str(csubject)+"', '"+str(cbody)+"', '"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"', FALSE);");
	rows = c.execute("insert into PUBLIC_COMPLAINTS values('"+str(uid)+"','"+str(cid)+"','"+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"');");
	conn.commit()
	c.close()'''
	return redirect(url_for('hello_world'))

if __name__=='__main__':
	app.run(debug=True)
