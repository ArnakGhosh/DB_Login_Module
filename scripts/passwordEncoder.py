import base64
import customException as CE
import loggerModule as LOG
def decoderpass(s):
	LOG.setup_logging_to_file()
	try:
		sup=base64.decodebytes(s.encode()).decode()
	except Exception as a:
		setattr(a,'message','Unsuccessful decryption')
		LOG.log_exception(a)
	else:
		return sup
def encoderpass(s):
	LOG.setup_logging_to_file()
	try:
		sup=base64.encodebytes(s.encode()).decode()
	except Exception as a:
		setattr(a,'message','Unsuccessful encryption')
		LOG.log_exception(a)
	else:
		return sup
if __name__ == '__main__':
	LOG.setup_logging_to_file(filename="../logs/user_encoder.log")
	try:
		pswd=input("Enter your password to be encrypted :\n")
		if len(pswd)>0:
			print(encoderpass(pswd))
		else:
			raise CE.UnsuccessfulEncryption(msg="Invalid password or blank")
	except Exception as a:
		setattr(a,'message','Calling UnsuccessfulEncryption')
		LOG.log_exception(a)
	finally:
		input()