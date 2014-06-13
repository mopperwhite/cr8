#!/usr/bin/python
#encoding=UTF-8

import re,random
def dictreplace(stri,dic):
	return reduce(lambda s,k:s.replace(k,dic[k]),[stri]+dic.keys())
def replace_html_linesep(s):
	return dictreplace(s,{'\n\r':'<br/>','\n':'<br/>','\r':'<br>'})
def levenshtein(first, second):  
	"""Find the Levenshtein distance between two strings."""  
	if len(first) > len(second):  
		first, second = second, first  
	if len(second) == 0:  
		return len(first)  
	first_length = len(first) + 1  
	second_length = len(second) + 1  
	distance_matrix = [range(second_length) for x in range(first_length)]  
	for i in range(1, first_length):  
		for j in range(1, second_length):  
			deletion = distance_matrix[i-1][j] + 1  
			insertion = distance_matrix[i][j-1] + 1  
			substitution = distance_matrix[i-1][j-1]  
			if first[i-1] != second[j-1]:  
				substitution += 1  
			distance_matrix[i][j] = min(insertion, deletion, substitution)
	return distance_matrix[first_length-1][second_length-1]
class RegexFormater(object):
	METACHARACTERS=r'\.^$*+?{}[]|/()'
	REGEX_FLAGS={'S':re.S,'I':re.I,'L':re.L,'M':re.M,'X':re.X}
	def __init__(self,format_,order,init_values={},get_dic={},format_dic={},regex_flag=''):
		if len(order)!=format_.count('%s'):
			raise Exception('The number of items in %r should be equal to the number of "%%s" in %r.'%(order,format_))
		self.formater=format_
		self.order=order
		self.init_values=map(lambda i:(i,''),order)+zip(init_values.keys(),init_values.values())
		self.get_dic=dict(map(lambda i:(i,lambda s:s),order)+zip(get_dic.keys(),get_dic.values()))
		self.format_dic=dict(map(lambda i:(i,lambda d:d[i]),order)+zip(format_dic.keys(),format_dic.values()))
		self.regex_flag=self.get_flags_from_str(regex_flag)
		self.regex=re.compile(self.transform_metacharacters(self.formater),self.regex_flag)
	@classmethod
	def transform_metacharacters(cls,s):
		return reduce(lambda s,i:s.replace(i,'\\'+i),[s]+list(cls.METACHARACTERS)).replace('%s','(.+?)')
	@classmethod
	def reverse_transform_metacharacters(cls,s):
		return reduce(lambda i:s.replace('\\'+i,i),[s.replace('(.+?)','%s')]+list(cls.METACHARACTERS))
	@classmethod
	def get_flags_from_str(cls,s):
		return reduce(lambda x,y:x|y,[0,0]+map(lambda s:cls.REGEX_FLAGS[s],s))
	def get(self,stri):
		l=map(lambda t:dict(self.init_values+zip(self.order,t)),self.regex.findall(stri))
		for i in l:
			for j in self.order:
				i[j]=self.get_dic[j](i[j])
		return l
	def format(self,dat,sep='\n'):
		return sep.join(map(lambda i:self.formater%tuple(map(lambda j:self.format_dic[j](i),self.order)),dat))
	def __call__(self,stri):
		return self.get(stri)
