#encoding=UTF-8
#注意请务必包含上一行
#本文件使用   UTF-8   编码
#这是一个可以用在CR里的插件
#在程序启动的时候运行以完成一些初始化的东西


#init.ini
#本目录下的init.ini文件的名字不能更改，其中的每个项目位置可以改变但都必须有
#"$."代表这个插件所在目录
'''
    [exec]
    mainfile=$./exe.py		#指定执行文件位置		
    [data]
    appdata=$./DATA		#指定数据存储文件夹位置，将被复制到用户的AppData文件夹下
    appsetting=$./setting.ini	#指定设置文件位置，将被复制到用户的AppSetting文件夹下
'''

print setting	#环境变量中将包含一个类字典对象以读取设置文件(setting.ini),可使用save()方法保存
print env	#环境变量中将包含一个类字典对象，用于显示数据文件夹的结构
print 'Hi,this is a CRApp.'	#随便做点什么

#CR的信号系统，在插件被加载的时候应该已经初始化完毕了
#CRSignal被放置在__builtin__模块中，可直接使用
#CRSignal.Connect(signal=信号(字符串，不可为空),target=一个可被调用的对象(比如函数),[调用时会传入的参数，可选])	绑定一个信号，对象不可调用或传入空字符串会导致绑定失败
#CRSignal.Send(signal=信号(字符串),[参数])或CRSignal(signal=信号(字符串),[参数])，发送一个信号，如果之前有传入参数，没名字的参数会被追加在之前的参数之后，有名字的会覆盖，返回调用之后的返回值
#CRSignal.SafeSend，与CRSignal.Send用法相同，如果出现异常将打印异常信息并返回None

#本地化
#_函数被放置在__builtin__模块中，可直接使用
#_(一个字符串,[用于格式化字符串的参数])，如果本地化文件中有可替换该字符串的字符串则返回本地化文件中的字符串，否则返回输入的字符串

#其他
#CRGlobal被放置在__builtin__模块中，可直接使用
#其中含有一些CR初始化的信息，不建议修改
