from dbconnector import connection
import hashlib as hl


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

def search_db(keyword):
	c,conn = connection()

	rows = c.execute("select * from COMPLAINTS")
	lis = []
	if rows > 0:
		res = c.fetchall()
		for i in range(len(res)):
			text = res[i][3]
			words = text.split(" ")
			if keyword in words:
				lis.append(res[i][0])
	return lis


re = search_db('blah')
print(re)