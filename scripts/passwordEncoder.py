#Added module for password encryption and decryption
#Encryption has been done to provide obscurity
#Should not be used for highly secured opertions
import base64
import customException as CE
import loggerModule as LOG
#decodes a given encrypted password to plain text
def decoderpass(s):
	LOG.setup_logging_to_file()
	try:
		sup=base64.decodebytes(s.encode()).decode()
	except Exception as a:
		setattr(a,'message','Unsuccessful decryption')
		LOG.log_exception(a)
	else:
		return sup.strip()
#encodes a given plain text into an obscured plain text
def encoderpass(s):
	LOG.setup_logging_to_file()
	try:
		sup=base64.encodebytes(s.encode()).decode()
	except Exception as a:
		setattr(a,'message','Unsuccessful encryption')
		LOG.log_exception(a)
	else:
		return sup.strip()
if __name__ == '__main__':
	LOG.setup_logging_to_file(filename="../logs/user_encoder.log")
	try:
		pswd=input("Enter your password to be encrypted :\n")
		if len(pswd)>0:
			print(encoderpass(pswd))
			logg="Password encoding successful"
		else:
			logg="Password encoding Unsuccessful"
			raise CE.UnsuccessfulEncryption(msg="Invalid password or blank")
	except Exception as a:
		setattr(a,'message','Calling UnsuccessfulEncryption')
		LOG.log_exception(a)
	finally:
		LOG.log_debug(logg)
		input()