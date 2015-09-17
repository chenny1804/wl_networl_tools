import serial
import sys
import string,time,os

class SerialInfo():
	__ser = ''
	def  __init__(self,dev,baudrate):
		self.__ser = serial.Serial(dev, baudrate,timeout=1)
	def getWlstat(self):
		currenttemperature=''
		tx_fail=''
		tx_fail_rep=''
		rx_with_crc=''
		rx_with_rep=''
		falsecck=''
		rssi_r=''
		rssi_l=''
		ampdu_tx_fail_count=''
		ampdu_tx_fail_rep=''
		cmd = 'iwpriv ra0 set ResetCounter=0;sleep 1;iwpriv ra0 stat\n\r'
		self.__ser.write(cmd)
		time.sleep(1)
		f=self.__ser.readlines()
		for line in f:
			if line.find('CurrentTemperature')!=-1:
				currenttemperature=line.split('=')[1].strip()
			if line.find('Tx fail count')!=-1:
				tx_fail=line.split('=')[1].strip().split(',')[0].strip()
				tx_fail_rep=line.split('=')[2].strip()
			if line.find('Rx with CRC')!=-1:
				rx_with_crc=line.split('=')[1].strip().split(',')[0].strip()
				rx_with_rep=line.split('=')[2].strip()
			if line.find('False CCA')!=-1:
				falsecck=line.split('=')[1].strip()
			if line.find('RSSI')!=-1:
				rssi_r=line.split('=')[1].strip().split()[0].strip()
				rssi_l=line.split('=')[1].strip().split()[1].strip()
			if line.find('AMPDU Tx fail count')!=-1:
				ampdu_tx_fail_count=line.split('=')[1].strip().split(',')[0].strip()
				ampdu_tx_fail_rep=line.split('=')[2].strip()
		return time.strftime('%Y\\%m\\%d %H\\%M\\%S',time.localtime(time.time()))+','+currenttemperature+','+falsecck+','+rssi_r+',' + rssi_l+ ',' + tx_fail+ ',' + \
		tx_fail_rep + ',' + rx_with_crc + ',' +rx_with_rep + ',' + ampdu_tx_fail_count + ',' + ampdu_tx_fail_rep
	
	def getStaInfo(self):
		flag=0
		intert=0
		sta_list=[]
		cmd = 'iwpriv ra0 show stainfo\n\r'
		self.__ser.write(cmd)
		f=self.__ser.readlines()
		for line in f:
			if len(line)>118 and len(line) < 125:
				#print len(line)
				#print len(line.split())
				list_line=line.split()
				if len(list_line)==18:
					print line
					sta_list.append(time.strftime('%Y\\%m\\%d %H\\%M\\%S',time.localtime(time.time()))+','+list_line[0].strip() + ',' + list_line[6].strip() + ',' + list_line[8].strip()+ ',' + list_line[9].strip() + ',' + list_line[13].strip())
				elif len(list_line) == 17:
					print line
					sta_list.append(time.strftime('%Y\\%m\\%d %H\\%M\\%S',time.localtime(time.time()))+','+list_line[0].strip() + ',' + list_line[6].strip().split('HTMIX')[0] + ',' + list_line[7].strip()+ ',' + list_line[8].strip() + ',' + list_line[12].strip())
		return sta_list
	
	def getMemInfo(self):
		cmd='cat /proc/meminfo\n\r'
		self.__ser.write(cmd)
		memfree=''
		memtotal=''
		f=self.__ser.readlines()
		for line in f:
			if line.find('MemTotal')!=-1:
				memtotal=line.split(':')[1].strip().split()[0]
			if line.find('MemFree')!=-1:
				memfree=line.split(':')[1].strip().split()[0]
		return time.strftime('%Y\\%m\\%d %H\\%M\\%S',time.localtime(time.time()))+','+ str(float(memfree)/float(memtotal)*100)+'%'

if __name__=='__main__':
	if os.path.exists("./wl_stat_info.csv"):
		wl_stat=open('./wl_stat_info.csv','a')
	else:
		wl_stat=open('./wl_stat_info.csv','a')
		wl_stat.write('time,CurrentTemperature,False CCA,rssi_l,rssi_r,Tx fail count,Tx fail count(PER),Rx with CRC,Rx with CRC(PER),AMPDU Tx fail count,AMPDU Tx fail count(PER)\n')
		wl_stat.flush()
	
	if os.path.exists("./wl_sta_info.csv"):
		wl_sta_info=open('./wl_sta_info.csv','a')
	else:
		wl_sta_info=open('./wl_sta_info.csv','a')
		wl_sta_info.write("time,MAC,RSSI0/1/2,BW,MCS,Rate\n")
		wl_sta_info.flush()
		
	if os.path.exists("./wl_mem_info.csv"):
		wl_mem_info=open('./wl_mem_info.csv','a')
	else:
		wl_mem_info=open('./wl_mem_info.csv','a')
		wl_mem_info.write("time,free mem\n")
		wl_mem_info.flush()
	serial=SerialInfo(sys.argv[1],57600)
	while True:
		time.sleep(int(sys.argv[2]))
		wl_stat.write(serial.getWlstat()+'\n')
		for line in serial.getStaInfo():
			wl_sta_info.write(line+'\n')
		wl_mem_info.write(serial.getMemInfo()+'\n')
		
		wl_stat.flush()
		wl_sta_info.flush()
		wl_mem_info.flush()
		print 'wirte log successly!'
