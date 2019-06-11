import os
import psycopg2
from psycopg2 import Error as DBERR
import loggerModule as LOG
import customException as CE
import passwordEncoder as PE
LOG.setup_logging_to_file()
def connModule():
	dbpp,dbp,fl='Start',list(),0
	try:
		with open('../properties/DB_DETAILS.properties','r') as db:
			while len(dbpp)!=0:
				dbpp=db.readlines(2)
				dbp.append(dbpp)
		dbp.pop()
		for i in range(6,11):
			if len(dbp[i])!=1:
				fl=1
				break
		if len(dbp)!=11 or fl!=0:
			raise CE.DBException(msg="Incorrect Properties file, check properties/DB_DETAILS.properties",dberr=str(DBERR.pgerror)+str(DBERR.pgcode))
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		'''print(dbp)'''
		dbhost=dbp[6][0][dbp[6][0].find(":")+1:].strip()
		dbport=int(dbp[7][0][dbp[7][0].find(":")+1:].strip())
		dbname=dbp[8][0][dbp[8][0].find(":")+1:].strip()
		dbuser=dbp[9][0][dbp[9][0].find(":")+1:].strip()
		dbpass=dbp[10][0][dbp[10][0].find(":")+1:].strip()
		dbpass=PE.decoderpass(dbpass)
		'''print(dbhost, dbport, dbname, dbuser, dbpass)'''
		try:
			conn=psycopg2.connect(user=dbuser, password=dbpass, host=dbhost, port=dbport, database=dbname)
		except Exception as a:
			setattr(a,'message','Calling Exception')
			LOG.log_exception(a)
		else:
			LOG.log_debug("Connection to {DB} DB is successful with {user} on {host}:{port}".format(DB=dbname,user=dbuser,host=dbhost,port=dbport))
			return conn
def cursModule(s):
	try:
		con=s
		cursr=con.cursor()
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("Cursor opened")
		return cursr
def closeCon(con, cur):
	try:
		con.close()
		cur.close()
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("Closed Connection to DB")
if __name__=='__main__':
	try:
		conn=connModule()
		crsr=cursModule(conn)
		qstr="SELECT version();"
		crsr.execute(qstr)
		rec=crsr.fetchall()
		LOG.log_debug("Submitted Query {query}, fetched results as {result}".format(query=qstr, result=rec))
		closeCon(conn, crsr)
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		print("\n\n",rec)