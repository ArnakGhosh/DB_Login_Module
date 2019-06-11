class MyExceptions(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)
class DBException(MyExceptions):
	def __init__(self,msg,dberr):
		self.__dberr=dberr
		MyExceptions.__init__(self,msg)
class UnsuccessfulEncryption(MyExceptions):
	def __init__(self,msg,err=0):
		self.__errstatus=err
		MyExceptions.__init__(self, msg)