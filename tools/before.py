import os,sys,time
sys.path.append("../")
from am import AndroidAm
from logcat import logcat
import subprocess

devices=[]

if __name__=='__main__':
	am=AndroidAm()
	logcat=logcat()
	
	os.system("adb devices > device_t")
	
	f=open('./device_t','r')
	for line in iter(f):
		if line.find("List")==-1 and line.find('device')!=-1:
			dev_id=line.split()[0]
			print dev_id
			devices.append(dev_id)
			am.startConnect(dev_id,"zhufangjian","123456789")
			am.stopConnect(dev_id)
			am.startEndpoint(dev_id)
	
	time.sleep(5)
	print '##################################'
	for dev_id in devices:
		cmd = []
		cmd.append('adb')
		cmd.append('-s')
		cmd.append(dev_id)
		cmd.append('shell')
		cmd.append('netcfg')
			

		fdp = subprocess.Popen( cmd, stdout = subprocess.PIPE )
			
		for line in fdp.stdout:
			if line.find("wlan0")!=-1:
				print dev_id+":"+line.split()[2].strip()
	f.close()
	os.system("del device_t")
	
	