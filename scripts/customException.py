#This Class is having Exception handling feature for different Modules
#MyExceptions has been derived from the base class Exception
class MyExceptions(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)
#DBException has been derived from MyExceptions,
#to handle DB related or connection related Exceptions
class DBException(MyExceptions):
	def __init__(self,msg,dberr):
		self.__dberr=dberr
		MyExceptions.__init__(self,msg)
#UnsuccessfulEncryption has been derived from MyExceptions
#This has been derived to handle password encryption
#exceptions while the user runs to encrypt their own DB password
#before changing in the DB_details.properties file
class UnsuccessfulEncryption(MyExceptions):
	def __init__(self,msg,err=0):
		self.__errstatus=err
		MyExceptions.__init__(self, msg)
#Exception for record not found in DB
class RecordNotFound(MyExceptions):
	def __init__(self,msg,record=''):
		self.__record=record
		MyExceptions.__init__(self, msg)
#Exception for Job found inactive
#Operation denied
class JobInactive(MyExceptions):
	def __init__(self,msg,jobid):
		self.__jobid=jobid
		MyExceptions.__init__(self, msg)
#Exception for invalid or expired password
class InvalidPassword(MyExceptions):
	def __init__(self,msg,status):
		self.__status=status
		MyExceptions.__init__(self, msg)
#Exception for User account expiry
class UserAccountExpired(MyExceptions):
	def __init__(self, msg, user):
		self.__user=user
		MyExceptions.__init__(self, msg)
#USER Authentication Exception
class UserAuthException(MyExceptions):
	def __init__(self, msg, flagg):
		self.__flagg=flagg
		MyExceptions.__init__(self, msg)