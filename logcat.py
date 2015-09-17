import subprocess
import os,sys
import string
import datetime

class logcat():
	def start(self,dev_n):
		#cmd = 'adb -s '+dev_n+' shell logcat -s XiaomiPlayerJNI:V'
		cmd = 'adb -s '+dev_n+' shell logcat -s VedioViewTest:V GETSTREAM:V'
		return subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	def stop(self,pid):
		os.system("taskkill /f /im "+str(pid))
	def startWifiInfo(self,dev_n):
		cmd = 'adb -s '+dev_n+' shell logcat -s [WifiAdmin]:V'
			
	

if __name__=='__main__':
	logcat=logcat()
	logcat.stop()