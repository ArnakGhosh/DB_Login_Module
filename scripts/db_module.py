#Module containing all the DB related Functions
#INSERT, UPDATE, CHECK and DELETE operations
import psycopg2
import loggerModule as LOG
import customException as CE
#import passwordEncoder as PE //applied for unit testing
import db_conn as DBC
import datetime
#Module for Checking existence of user in table
#Returns 2 if user is present and and valid
#Returns 1 if user is present but validity has expired
#Returns 0 if user is not present
def checkuser(s):
	query="SELECT CASE WHEN u_id='{idd}' and u_valid>now()::timestamp Then 2 WHEN u_id='{idd}' and u_valid<now()::timestamp Then 1 ELSE 0 END from udet where u_id='{idd}';".format(idd=s)
	try:
		(cn,cr)=dbquery(query)
		rec=cr.fetchall()
		if len(rec)!=0:
			if rec[0][0]==2:
				fl=0
			elif rec[0][0]==1:
				fl=1
				raise CE.UserAccountExpired(msg='Account has expired for user {u}'.format(u=s), user=s)
		else:
			fl=1
			raise CE.RecordNotFound(msg='Record missing in DB', record=s)
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("Record Fetched successfully")
	finally:
		cn.commit()
		DBC.closeCon(cn, cr)
		if len(rec)!=0:
			return int(rec[0][0])
		else:
			return 0
#For all the DB queries in this module
#returns a connection and a cursor object after executing the query
def dbquery(s):
	try:
		conn=DBC.connModule()
		cur=DBC.cursModule(conn)
		LOG.log_debug("Query : {q}".format(q=s))
		cur.execute(s)
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		return conn,cur
#To check in UOPS table if INSERT (op_id=1)
#UPDATE (op_id=2) or DELETE (op_id=3)
#is enabled (op_inac=0) or Disabled(otherwise)
def checkjobsts(opid):
	fl,query=-1,"SELECT op_inac from uops where op_id={idd};".format(idd=opid)
	try:
		(cn,cr)=dbquery(query)
		rec=cr.fetchall()
		if rec[0][0]!=0:
			fl=1
			raise CE.JobInactive(msg="job Id {idd} found inactive".format(idd=opid),jobid=opid)
		else:
			fl=0
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("Job id {idd} found active.".format(idd=opid))
	finally:
		cn.commit()
		DBC.closeCon(cn, cr)
	if fl==0: return True
	else: return False
#To populate with the changes in ULOG table
#after every INSERT, UPDATE or DELETE from module	
def crudlog(opid,opstrt,opend,opsts,operr=None):
	if operr==None:
		query="INSERT INTO ULOG (op_id, op_start, op_end, op_status, op_error) values ({opid},'{opstrt}','{opend}','{opsts}',null)".format(opid=opid,opstrt=opstrt,opend=opend,opsts=opsts)
	else:
		query="INSERT INTO ULOG (op_id, op_start, op_end, op_status, op_error) values ({opid},'{opstrt}','{opend}','{opsts}','{operr}')".format(opid=opid,opstrt=opstrt,opend=opend,opsts=opsts,operr=operr)
	try:
		(cn,cr)=dbquery(query)
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	finally:
		cn.commit()
		DBC.closeCon(cn, cr)
#To add entry in UHIST table whenever
#there is a password change
def updatepasshist(uid,paswd,dy=0):
	query="INSERT INTO uhist (u_id, u_pass, u_valid_from, u_valid_till) values ('{u}','{p}','{vf}','{vt}');".format(u=uid,p=paswd,vf=str(datetime.datetime.now()),vt=str(datetime.datetime.now()+datetime.timedelta(days=dy)))
	try:
		(cn,cr)=dbquery(query)
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("Update Password history successful")
	finally:
		cn.commit()
		DBC.closeCon(cn, cr)
#To reset password of a user		
def resetPassword(uid):
	defpaswd=PE.encoderpass('Kolkata@1')
	vf,bl=str(datetime.datetime.now()),None
	query="UPDATE ucred set u_pass='{ps}',u_reset=1 where u_id='{u}';".format(ps=defpaswd,u=uid)
	try:
		bl=checkjobsts(2)
		if bl:
			(cn, cr)=dbquery(query)
			opsts="SUCCESS"
			operr=None
			loggg="Password reset successful for {opid}.".format(opid=uid)
			updatepasshist(uid,defpaswd,dy=2)
		else:
			LOG.log_debug("Job id {idd} found inacactive.".format(idd=2))
			opsts="FAILURE"
			operr="Job id {idd} found inacactive.".format(idd=2)
			loggg="Password reset unsuccessful for {opid}.".format(opid=uid)
	except Exception as a:
		opsts="FAILURE"
		operr=str(a.__class__)
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug(loggg)
	finally:
		endd=str(datetime.datetime.now())
		crudlog(opid=2,opstrt=vf,opend=endd,opsts=opsts,operr=operr)
		if bl:
			cn.commit()
			DBC.closeCon(cn, cr)
#To check if a given password is present in UHIST
#and the validity has not expired for the last entry
#returns 1 if present and valid
#returns 0 otherwise
def validatepasshist(uid,paswd):
	query,logg="SELECT CASE WHEN u_valid_till>now()::timestamp Then 1 ELSE 0 END from uhist where u_id='{u}' and u_pass='{p}' order by u_valid_from desc;".format(u=uid,p=paswd),''
	try:
		(cn,cr)=dbquery(query)
		rec=cr.fetchall()
		if rec[0][0]==1:
			logg="Password is valid"
		else:
			logg="Password is either invalid or expired"
			raise CE.InvalidPassword(msg=logg,status=rec[0][0])
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	finally:
		LOG.log_debug(logg)
		cn.commit()
		DBC.closeCon(cn, cr)
		return int(rec[0][0])
#To change the password of a given user
def changepassword(uid,npass):
	query,fl,bl,strt="UPDATE ucred set u_pass='{p}', u_reset=0 where u_id='{u}';".format(p=npass,u=uid),-1,None,str(datetime.datetime.now())
	try:
		bl=checkjobsts(2)
		if bl:
			(cn,cr)=dbquery(query)
			logg,fl="Password changed successfully for user {u}".format(u=uid),0
			opsts,operr='SUCCESS',None
			updatepasshist(uid,npass,dy=90)
		else:
			LOG.log_debug("Job id {idd} found inacactive.".format(idd=2))
			opsts="FAILURE"
			operr="Job id {idd} found inacactive.".format(idd=2)
			logg="Password reset unsuccessful for {opid}.".format(opid=uid)
	except Exception as a:
		logg,fl="Password could not be changed for user {u}".format(u=uid),1
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug(logg)
	finally:
		endd=str(datetime.datetime.now())
		crudlog(opid=2,opstrt=strt,opend=endd,opsts=opsts,operr=operr)
		if bl:
			cn.commit()
			DBC.closeCon(cn, cr)
		return fl
#To insert a new user in the system
def userInsert(uid,unm,doj,uval,umail='NA',ucont='NA'):
	bl,fl,logg,strt,opsts,operr=None,-1,'',str(datetime.datetime.now()),'',''
	if checkuser(s=uid)==0:
		query1="INSERT INTO udet (u_id,u_name,u_doj,u_valid,u_mail,u_cont) values ('{u}','{nm}','{dj}','{vl}','{ml}','{ct}');".format(u=uid,nm=unm,dj=doj,vl=uval,ml=umail,ct=ucont)
		query2="INSERT INTO ucred (u_id,u_pass,u_retry,u_reset) values ('{u}','NA',0,0);".format(u=uid)
		try:
			bl=checkjobsts(1)
			if bl:
				(cn1,cr1)=dbquery(query1)
				cn1.commit()
				(cn2,cr2)=dbquery(query2)
				cn2.commit()
				opsts,operr='SUCCESS',None
				resetPassword(uid)
				logg,fl="User {u} has been added successfully".format(u=uid),0
			else:
				LOG.log_debug("Job id {idd} found inacactive.".format(idd=1))
				opsts,operr="FAILURE","Job id {idd} found inacactive.".format(idd=1)
				logg="Database Entry unsuccessful for {opid}.".format(opid=uid)
		except Exception as a:
			logg,fl="Database Entry unsuccessful for {u}".format(u=uid),1
			opsts,operr="FAILURE",str(a.__class__)
			setattr(a,'message','Calling Exception')
			LOG.log_exception(a)
		else:
			LOG.log_debug(logg)
		finally:
			if fl==0:
				cn1.commit()
				DBC.closeCon(cn1, cr1)
				cn2.commit()
				DBC.closeCon(cn2, cr2)
	elif checkuser(s=uid)==1:
		opsts,operr="FAILURE","Database Entry unsuccessful for {opid}. User account has expired".format(opid=uid)
	else:
		opsts,operr="FAILURE","Database Entry unsuccessful for {opid}. User account is already present".format(opid=uid)
#To fetch the userdetails in case of search
#or other purpose
def getuserDetails(uid):
	query="SELECT u_name,u_doj,u_valid,u_mail,u_cont from udet where u_id='{u}';".format(u=uid)
	try:
		(cn,cr)=dbquery(query)
		rec=cr.fetchall()
		cn.commit()
	except Exception as a:
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("User details fetched successfuly")
	finally:
		DBC.closeCon(cn, cr)
	return rec
#To update an existing record of an user
def userUpdate(uid,unm=None,uval=None,umail=None,ucont=None):
	bl,fl,logg,strt,opsts,operr=None,-1,'',str(datetime.datetime.now()),'',''
	if checkuser(s=uid)==2:
		rec=getuserDetails(uid)
		unm=rec[0][0] if unm==None else unm
		uval=str(rec[0][2]) if uval==None else uval
		umail=rec[0][3] if umail==None else umail
		ucont=rec[0][4] if ucont==None else ucont
		query="UPDATE udet SET u_name='{u}',u_valid='{v}',u_mail='{w}',u_cont='{x}' where u_id='{idd}';".format(u=unm,v=uval,w=umail,x=ucont,idd=uid)
		try:
			bl=checkjobsts(2)
			if bl:
				(cn,cr)=dbquery(query)
				cn.commit()
				opsts,operr='SUCCESS',None
				logg,fl="User {u} has been updated successfully".format(u=uid),0
			else:
				LOG.log_debug("Job id {idd} found inacactive.".format(idd=2))
				opsts,operr="FAILURE","Job id {idd} found inacactive.".format(idd=2)
				logg="Database Update unsuccessful for {opid}.".format(opid=uid)
		except Exception as a:
			logg,fl="Database Update unsuccessful for {u}".format(u=uid),1
			opsts,operr="FAILURE",str(a.__class__)
			setattr(a,'message','Calling Exception')
			LOG.log_exception(a)
		else:
			LOG.log_debug(logg)
		finally:
			if fl==0:
				cn.commit()
				DBC.closeCon(cn, cr)
	elif checkuser(s=uid)==1:
		opsts,operr="FAILURE","Database Update unsuccessful for {opid}. User account has expired".format(opid=uid)
	else:
		opsts,operr="FAILURE","Database Update unsuccessful for {opid}. User account is not present".format(opid=uid)
	endd=str(datetime.datetime.now())
	crudlog(opid=2,opstrt=strt,opend=endd,opsts=opsts,operr=operr)
#to delete an existing user
#user may be valid or validity might have been expired
def userDelete(uid):
	bl,fl,logg,strt,opsts,operr,ustat,rec=None,-1,'',str(datetime.datetime.now()),'','',checkuser(s=uid),None
	if ustat==2 or ustat==1:
		rec=getuserDetails(uid)
		query1="DELETE from ucred where u_id='{idd}';".format(idd=uid)
		query2="DELETE from udet where u_id='{idd}';".format(idd=uid)
		try:
			bl=checkjobsts(3)
			if bl:
				(cn1,cr1)=dbquery(query1)
				cn1.commit()
				(cn2,cr2)=dbquery(query2)
				cn2.commit()
				opsts,operr='SUCCESS',None
				logg,fl="User {u} has been deleted successfully".format(u=uid),0
			else:
				LOG.log_debug("Job id {idd} found inacactive.".format(idd=3))
				opsts,operr="FAILURE","Job id {idd} found inacactive.".format(idd=3)
				logg="delete record from Database unsuccessful for {opid}.".format(opid=uid)
		except Exception as a:
			logg,fl="delete from Database unsuccessful for {u}".format(u=uid),1
			opsts,operr="FAILURE",str(a.__class__)
			setattr(a,'message','Calling Exception')
			LOG.log_exception(a)
		else:
			LOG.log_debug(logg)
		finally:
			if fl==0:
				cn1.commit()
				DBC.closeCon(cn1, cr1)
				cn2.commit()
				DBC.closeCon(cn2, cr2)
	else:
		opsts,operr="FAILURE","delete from Database unsuccessful for {opid}. User account is not present".format(opid=uid)
	endd=str(datetime.datetime.now())
	crudlog(opid=3,opstrt=strt,opend=endd,opsts=opsts,operr=operr)
	return rec
#To authenticate user, based on User id and given password
#Returns the following
#'AXP' - if user validity has expired, based on UDET(u_valid)
#'ANP' - if user account is not present in the system
#'PXP' - if password has expired or not present based on UHIST(u_valid_till)
#'PRS' - if password reset flag has been set by module, or otherwise, based on UCRED(u_reset)
#'PWR' - if password is wrong based on UCRED(u_pass)
#'ASC' - if all the criteria is satified and on successful authentication
def authenticateUser(uid, paswd):
	rfl,fl,userdict,pashist,rstdict,pmdict,rec=None,0,{0:'ANP',1:'AXP',2:'GO'},{0:'PXP',1:'GO'},{0:'GO',1:'PRS'},{0:'GO',1:'PWR'},None
	query1="select CASE when u_reset=0 then 0 else 1 end from ucred where u_id='{u}';".format(u=uid)
	query2="select CASE when u_pass='{p}' then 0 else 1 end from ucred where u_id='{u}';".format(p=paswd,u=uid)
	try:
		rfl=userdict[checkuser(s=uid)]
		fl+=1
		if rfl!='GO':
			raise CE.UserAuthException(msg="User Not Authenticated",flagg=rfl)
		rfl=pashist[validatepasshist(uid,paswd)]
		fl+=1
		if rfl!='GO':
			raise CE.UserAuthException(msg="User Not Authenticated",flagg=rfl)
		(cn1,cr1)=dbquery(query1)
		cn1.commit()
		rec=cr1.fetchall()
		rfl=rstdict[rec[0][0]]
		fl+=1
		if rfl!='GO':
			raise CE.UserAuthException(msg="User Not Authenticated",flagg=rfl)
		(cn2,cr2)=dbquery(query2)
		cn2.commit()
		rec=cr2.fetchall()
		rfl=pmdict[rec[0][0]]
		fl+=1
		if rfl!='GO':
			raise CE.UserAuthException(msg="User Not Authenticated",flagg=rfl)
	except Exception as a:
		LOG.log_debug("user not authenticated")
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		LOG.log_debug("user authenticated successfully")
		rfl='ASC' if rfl=='GO' else rfl
	finally:
		if fl>2:
			DBC.closeCon(cn1, cr1)
		if fl>3:
			DBC.closeCon(cn2, cr2)
	return rfl
if __name__=='__main__':
	LOG.setup_logging_to_file()
	try:
		strt=str(datetime.datetime.now())
#		print(checkuser(s="doejohn02"))
#		resetPassword(uid='doejane01')
#		print(validatepasshist(uid='doejane01',paswd=PE.encoderpass('Kolkata@1')))
#		print(changepassword(uid='doejane01',npass=PE.encoderpass('Baranagar@123')))
#		userInsert(uid='dalisal01',unm='Salvador Dali',doj=str(datetime.datetime.now()),uval=str(datetime.datetime.now()+datetime.timedelta(days=2)),umail='NA',ucont='NA')
#		print(checkuser(s="dalisal01"))
#		userUpdate(uid="dalisal01",umail='giraffe@mail.com')
#		print(userDelete(uid="dalisal01"))
		print(authenticateUser(uid='doejohn01', paswd='S29sa2F0YUAx'))
	except Exception as a:
		endd=str(datetime.datetime.now())
		crudlog(opid=1,opstrt=strt,opend=endd,opsts="UNIT_CHECK",operr="ERROR "+str(a.__class__))
		setattr(a,'message','Calling Exception')
		LOG.log_exception(a)
	else:
		endd=str(datetime.datetime.now())
		crudlog(opid=1,opstrt=strt,opend=endd,opsts="UNIT_CHECK")