#logger module
import sys
import traceback
import logging
import os
#for initialisation of the logging file
#will create a directory in the root path of the 
#distribution if not present
def setup_logging_to_file(filename="../logs/pyth_error.log"):
	if os.path.exists("../logs"):
		logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s',)
	else:
		os.mkdir("../logs",0o755)
		logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s',)
#Extracts the Exception class name from traceback stack
def extract_function_name():
	tb = sys.exc_info()[-1]
	stk = traceback.extract_tb(tb, 1)
	fname = stk[0][3]
	return fname
#For logging the exceptions
def log_exception(e):
	logging.error("Function {function_name} raised {exception_class} ({exception_docstring}) : {exception_message}".format(
	function_name=extract_function_name(),
	exception_class=e.__class__,
	exception_docstring=e.__doc__,
	exception_message=e.message))
#For logging general debug messages
def log_debug(e):
	logging.debug(e)
if __name__=='__main__':
	setup_logging_to_file()