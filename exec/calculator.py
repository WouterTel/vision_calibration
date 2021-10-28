import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

message = ""

def py_setMsg(msg):
	global message
	message	= msg
	return message
	
def py_getMsg():
	temp = ""
	if str(message):
		temp = message
	else:
		temp = "(no message)"
	return temp
	
def py_add(a, b):
	z = a + b
	return z

def py_subtract(a, b):
	z = a - b
	return z

def py_divide(a, b):
	z = a / b
	return z
	
def py_multiply(a, b):
	z = a * b
	return z

print("XMLRPC Server started..")

server = SimpleXMLRPCServer(("localhost", 60050))
server.register_function(py_setMsg, "ext_setMsg")
server.register_function(py_getMsg, "ext_getMsg")
server.register_function(py_add, "ext_add")
server.register_function(py_subtract, "ext_subtract")
server.register_function(py_divide, "ext_divide")
server.register_function(py_multiply, "ext_multiply")
server.serve_forever()

