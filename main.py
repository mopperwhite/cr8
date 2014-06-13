#!/usr/bin/python
#encoding=UTF-8

import chattingrobot,os
if __name__=='__main__':
	app=chattingrobot.ChattingRobotApp(os.path.join(os.getcwdu(),'init.ini'))
	app.exec_()