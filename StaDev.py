
# -*- coding: utf-8 -*- 
from am import AndroidAm
from logcat import logcat
import os,sys
import string

"""关于设备的一些操作"""

class StaDev():
	_id=''
	_dev_name=''
	_playurl=''
	_logcatprocess=''
	_stepfile=''
	_priority=''
	_am=AndroidAm()
	_logcat=logcat()
	def __init__(self,id,dev_name,playurl,priority):
		self._id=id
		self._playurl=playurl
		self._priority=priority
		self._dev_name=dev_name
	"""获取设备型号名"""
	def GetDevName(self):
		return self._dev_name
	"""获取设备优先级"""
	def GetPriority(self):
		return self._priority
	"""获取设备ID"""
	def GetId(self):
		return self._id
	"""获取设备播放地址"""
	def GetPlayUrl(self):
		return self._playurl
	"""获取设备日志输出进程号"""
	def GetLogCatProcess(self):
		return self._logcatprocess
	"""打开设备默认浏览器"""
	def OpenBrowser(self):
		print 'open brower ' + self._id + '\n'
		self._am.startBrowser(self._playurl,self._id)
	"""关闭设备默认浏览器"""
	def StopBrowser(self):
		print 'stop brower ' + self._id + '\n'
		self._am.stopBrowser(self._id)
	"""打开设备播放器"""
	def OpenPlayer(self):
		print 'open Player ' + self._id + '\n'
		self._am.startPlayer(self._playurl,self._id)
	"""关闭设备播放器"""
	def StopPlayer(self):
		print 'stop Player ' + self._id + '\n'
		self._am.stopPlayer(self._id)
	"""根据步奏操作设备网页"""
	def StartPlay(self):
		print 'start play ' + self._id + '\n'
		os.popen("monkeyrunner "+str(os.getcwd())+"\\startplay.py " + self._id + ' ' + self._stepfile)
	"""打开设备日志输出"""
	def OpenLogCat(self):
		print 'open log cat ' + self._id + '\n'
		self._logcatprocess=self._logcat.start(self._id)
	"""关闭设备日志输出"""
	def StopLogCat(self):
		print 'stop log cat ' + self._id + '\n'
		self._logcat.stop(self._logcatprocess.pid)