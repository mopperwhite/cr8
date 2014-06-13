#!/usr/bin/python
#encoding=UTF-8

import urllib,json,time,webbrowser,re
def get_data_from_tieba(pid):
    def the_last_page(data):
	return u'</head><body><div>您要浏览的贴子不存在<br/>' in data
    def get_data():
	p=1
	while True:
	    data=urllib.urlopen("http://wapp.baidu.com/mo/m?kz=%s&pn=%d"%(pid,10*(p-1))).read().decode('utf-8')
	    if the_last_page(data):return 
	    yield data
	    p+=1
    return reduce(lambda x,y:x+'\n'+y,get_data())
def get_weather(code):
	    #~ funcid='cr_get_weather'
	    #~ cache=CRCache()
	    #~ if funcid in cache and time.strftime("%D",cache[funcid].localmtime())==time.strftime("%D",time.localtime(time.time())):
		#~ data=cache[funcid].getvalue()
	    #~ else:
		#~ data=urllib.urlopen('http://www.weather.com.cn/data/cityinfo/%s.html'%code).read()
		#~ cache.register(funcid,data)
		#~ cache.edit(funcid,data)
	    #~ print json.loads(data)
	    data=urllib.urlopen('http://www.weather.com.cn/data/cityinfo/%s.html'%code).read()
	    return json.loads(data)['weatherinfo']
	
def get_ip():
	return json.loads(urllib.urlopen('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json'%code).read())
def search_google(messager):
	webbrowser.open_new_tab('http://www.google.com.hk/#&ie=utf-8&q=%s'%urllib.quote_plus(re.sub(messager.key.value,'',messager.string).encode('utf-8').replace('<br/>','')))

func_list=[get_data_from_tieba,get_weather,get_ip,search_google]
for f in func_list:
    CRSignal.connect('cr.%s'%f.func_name,f)
