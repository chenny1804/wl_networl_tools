# -*- coding: utf-8 -*- 
from StaDev import StaDev
import subprocess
import time,os,sys,string
import threading
import datetime
import shutil
import SimpleXMLRPCServer
import multiprocessing
import csv


thread={}
StaDevArray=[]

LOGPATH='./log/'
   
def copylog():
	dir=LOGPATH+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	if not os.path.exists(dir):
		print 'copy file'
		os.mkdir(dir)
	for file in os.listdir(LOGPATH):
		if file.find('csv')!=-1:
			shutil.move(LOGPATH+file,dir) 
			
def ishaveid(dev_id):
	f=open('./device_t','r')
	for line in iter(f):
		if line.find(dev_id)!=-1:
			f.close()
			return True
	f.close()
	return False
	
def getlogtime(time_t=0):
	if time_t==0:
		return time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
	else:
		return time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time_t))


#解决大量调用subprocess.Popen产生 "Too many open files"这个异常	
def wait_stop(stadev):
	process=stadev.GetLogCatProcess()
	print "-------1----------"
#	try:
#		process.terminate()
#	except Exception,e:
#		return None
	print "-------2----------"
	#out = process.communicate()[0]
	#if process.stdin:
	#	process.stdin.close()
	if process.stdout:
		process.stdout.close()
	#if process.stderr:
		#process.stderr.close()
	
	print "-------3----------"
	try:
		process.kill()
	except OSError:
		pass
		
	print "-------4----------"
	return out

def AnalysisThread(stadev):
	n=0
	m=0
	flag=0
	start_time=''
	end_time=''
	start_delay=''
	if stadev.GetId().find('/'):
			filename=stadev.GetId().replace("/","_")
	else:
		filename=stadev.GetId()
	if os.path.exists(LOGPATH+filename +'_delay.csv'):
		bug=open(LOGPATH+filename +'_delay.csv','a+')
	else:
		bug=open(LOGPATH+filename +'_delay.csv','a+')
		bug.write("date,delay time\n")
		bug.flush()
	
	if os.path.exists(LOGPATH+filename +'_stream.csv'):
		stream=open(LOGPATH+filename +'_stream.csv','a+')
	else:
		stream=open(LOGPATH+filename +'_stream.csv','a+')
		stream.write("date,flow\n")
		stream.flush()
		
	if os.path.exists(LOGPATH+stadev.GetId() +'_wait.csv'):
		wait_info=open(LOGPATH+filename+'_wait.csv','a+')
	else:
		wait_info=open(LOGPATH+filename+'_wait.csv','a+')
		wait_info.write("date,waiting time\n")
		wait_info.flush()
	old_ms=''
	new_ms=''
	
	stadev.StopPlayer()
	stadev.OpenLogCat()
	stadev.OpenPlayer()
	#点击播放器开始的时间
	start_click_time=time.time()
	
	while True:
		for line in iter(stadev.GetLogCatProcess().stdout.readline, ''):
			if line.rstrip().find('VedioViewTest')==-1:
				if line.rstrip().find('GETSTREAM')!=-1:
					stream.write(line.split(":")[1].strip()+'\n')
			else:
				#小米盒子和手机的输出信息格式不统一
				if stadev.GetDevName()=="xiaomihezi":
					new_ms=line.split()[3].strip()
				else:
					new_ms=line.split(":")[1].strip()
					
				#当时间值有值及小于500时视为播放器开始播放，因为大于500有可能是上一次播放的缓存信息
				
				#if stadev.GetId()=='10317/180849633':
				#	print old_ms + " " + new_ms 
				if old_ms!='' and old_ms!=new_ms:#and int(new_ms) < 500:
					if flag==0:
						start_play_time=time.time()
						wait_info.write(getlogtime(start_click_time) + ',' + getlogtime(start_play_time) + ',' + str(start_play_time-start_click_time)+"\n")
						flag=1
						
				#位置相同视为继续卡顿，不同及重新计数并将卡顿信息写入日志
				if old_ms==new_ms:
					m=m+1
				else:
					if m>5:
						end_time=time.time()
						a=end_time-start_time
						#只有卡顿时间大于0.1s才写入日志
						if float(a)>0.1:
							bug.write(start_delay+','+getlogtime()+','+str(a)+"\n")
					m=0
				#出现5次相同位置及被视为卡顿并记录开始卡顿时间
				if m>5:
					if m==6:						
						start_time=time.time()
						start_delay=getlogtime(start_time)
				old_ms=new_ms
			bug.flush()
			stream.flush()
			wait_info.flush()
			if thread[stadev.GetId()] == 0:
				stadev.GetLogCatProcess().stdout.flush()
				stadev.GetLogCatProcess().stdout.close()
				stadev.StopPlayer()
				stadev.StopLogCat()
				bug.flush()
				bug.close()
				stream.flush()
				stream.close()
				wait_info.flush()
				wait_info.close()
				return
				

def StartDevice(period,interval):

	os.system("adb devices > device_t")
	f=open('./devices_client.csv','r')
	reader = csv.reader(f)
	#从配置文件读取设备信息，将其写入设备列表中
	for row in reader:
		if ishaveid(row[0]):
			StaDevArray.append(StaDev(row[0],row[1],row[2],row[3]))
	f.close()
	while True:
		os.system('taskkill /f /im adb.exe')
		#根据设备列表中设备的优先级，先后启动设备
		for j in range(1,3):
			print j
			for i in StaDevArray:
				print "sta Priority : " + i.GetPriority()
				if i.GetPriority() == str(j):
					print 'start the thread\n'
					thread[i.GetId()] = 1
					new_thread = threading.Thread(target=AnalysisThread,args=(i,))
					new_thread.start()
			time.sleep(string.atoi(interval))
		
		
		print "wait for play\n"
		time.sleep(string.atoi(period)*60)
		
	#	for i in StaDevArray:
		#	wait_stop(i)
		
		#关闭所有设备线程
		for i in thread:
			thread[i] = 0
		
		print 'sleep 20\n'
		time.sleep(20)
		

def startDev(device_list,period,interval):
	print "start Dev"
	#将控制端配置文件写入本地
	f=open('./devices_client.csv','w')
	for line in device_list:
#		print line
		f.write(line)
	
	f.flush()
	f.close()
	
	time.sleep(5)
	
	p = multiprocessing.Process(target=StartDevice, args=(period,interval))
	p.start()
	return "SUCCESS"
	
def stopDev():
	pid_file=open('./pid','r')
	line=pid_file.readline()
	print line.strip()
	os.system("taskkill /f /im "+ line.strip())
	
	pid_file.close()
	return "SUCCESS"

if __name__=='__main__':
	copylog()
#	server = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', 28888))
	server = SimpleXMLRPCServer.SimpleXMLRPCServer((sys.argv[1], 28888))
	server.register_function(startDev)
	server.register_function(stopDev)
	server.serve_forever()