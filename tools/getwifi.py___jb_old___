import sys,os

def ishaveid(dev_id):
	f=open('./device_t','r')
	while True:
		line=f.readline()
		if line:
			if line.find(dev_id)!=-1:
				f.close()
				return True
		else:
			f.close()
			break 
	return False

f=open('./devices.log','r')
while True:
			line=f.readline()
			if line:
				if line.find('List')==-1 and line.find('device')!=-1:
						print line.split()[0].strip()
						dev_id=line.split()[0].strip().split(':')[0]
						if ishaveid(dev_id):
							os.system("adb -s "+dev_id+" shell cat /sdcard/dectect.txt > " + dev_id + "_wifi.csv")
				else:
						print 'error'
			else:
				f.close()
				break 