'''This Class is having Exception handling feature for different Modules'''
'''MyExceptions has been derived from the base class Exception'''
class MyExceptions(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)
'''DBException has been derived from MyExceptions,
to handle DB related or connection related Exceptions'''
class DBException(MyExceptions):
	def __init__(self,msg,dberr):
		self.__dberr=dberr
		MyExceptions.__init__(self,msg)
'''UnsuccessfulEncryption has been derived from MyExceptions
This has been derived to handle password encryption
exceptions while the user runs to encrypt their own DB password
before changing in the DB_details.properties file'''
class UnsuccessfulEncryption(MyExceptions):
	def __init__(self,msg,err=0):
		self.__errstatus=err
		MyExceptions.__init__(self, msg)
