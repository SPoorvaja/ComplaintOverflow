from dbconnector import connection
# c,conn = connection()

def auth_user(username, password):
	c,conn = connection()
	ct = c.execute("select p_pwd from USER where p_uid='"+username+"'")
	if ct>0:
		res = c.fetchall()  
		for row in res:
			pwd = row[0]
			if(pwd == password):
				return True
			else:
				return False
		return False

def register_user(username, first_name, last_name, ):
#auth_user('abc','def')