from dbconnector import connection
import hashlib as hl

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

#def register_user(username, first_name, last_name, ):
#auth_user('abc','def')
def register_user(username, first_name, last_name, dob, phone, email,addr1,addr2,pincode, city, state, password ):
#auth_user('abc','def')
	c,conn = connection()
	#ins = c.execute("insert into SCHEMES values (%s,%s,%s,%s)",(esc(name),esc(description),esc(eligibility),esc(category)))

	rowcount1 = c.execute("select * from USER where p_uid='" + username  + "'")
	if rowcount1>0:
		return False
	rowcount2 = c.execute("select * from USER where p_ph='" + phone  + "'")
	if rowcount2>0:
		return False
	ins = c.execute("insert into USER values (?,?,?,?,?,?,?,?,?,?,?,?)",(username, first_name, last_name, dob, phone, email,addr1,addr2,pincode, city, state, password  ))
	conn.commit()
	c.close()

def search_db(keyword):
	c,conn = connection()

	rows = c.execute("select * from COMPLAINTS")
	if rows > 0:
		lis = []
		res = c.fetchall()
		for i in range(len(res)):
			text = res[i][3]
			words = r.split(" ")
			if text in words:
				lis.append([res[i][0], res[i][1], res[i][2], res[i][3], res[i][4], res[i][5], res[i][6]])
	return lis

