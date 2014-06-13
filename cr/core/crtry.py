#!/usr/bin/python
#encoding=UTF-8

import traceback,StringIO,sys,types
def run(func,*args,**kwargs):
	try:
		return func(*args,**kwargs)
	except:
		traceback.print_exc()
		return None
def gettraceback():
	s=StringIO.StringIO()
	traceback.print_exc(file=s)
	return s.getvalue()

def getclassname(obj):
	if type(obj) in (types.ClassType,types.TypeType):
		return obj.__name__
	elif type(obj)==types.InstanceType:
		return obj.__class__.__name__
	else:
		return type(obj).__name__
def checktype(name,object_,type_,raise_exception=True):
	if type(type_)!=tuple:
		type_=(type_,)
	if (object_ is None and None in type_) or isinstance(object_,tuple(t for t in type_ if t is not None)):
		return True
	elif not raise_exception:
		return False 
	else:
		raise TypeError('"%s" must be %s , not %s.'%(name,' or '.join(getclassname(t) for t in type_),getclassname(object_)))
