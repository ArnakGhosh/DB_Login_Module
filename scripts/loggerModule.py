import sys
import traceback
import logging
import os
def setup_logging_to_file(filename="../logs/pyth_error.log"):
	if os.path.exists("../logs"):
		logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s',)
	else:
		os.mkdir("../logs",0o755)
		logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s',)
def extract_function_name():
	tb = sys.exc_info()[-1]
	stk = traceback.extract_tb(tb, 1)
	fname = stk[0][3]
	return fname
def log_exception(e):
	logging.error("Function {function_name} raised {exception_class} ({exception_docstring}) : {exception_message}".format(
	function_name=extract_function_name(),
	exception_class=e.__class__,
	exception_docstring=e.__doc__,
	exception_message=e.message))
def log_debug(e):
	logging.debug(e)
if __name__=='__main__':
	setup_logging_to_file()