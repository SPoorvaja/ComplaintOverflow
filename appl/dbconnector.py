import MySQLdb

def connection():
	conn=MySQLdb.connect(host="localhost",user="root",passwd="pattu",db="CLP")
	c = conn.cursor()
	return c,conn
