import MySQLdb

def connection():
	conn=MySQLdb.connect(host="localhost",user="root",passwd="passw0rd",db="CLP")
	c = conn.cursor()
	return c,conn
