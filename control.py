# -*- coding: utf-8 -*- 
import xmlrpclib
from StaDev import StaDev
import time,os,sys,string
import getopt

StaDevArray=[]
server_list=[]
period=0
interval=0
stop=0
flag=''

#-p 每一轮的间隔时间 -i 不同优先级之间的间隔时间
if __name__=='__main__':

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:i:s", ["help","period=","interval=","stop="])
	except getopt.GetoptError:
		print "getopt error!"
	for o,a in opts:
		if o in ("-p","--period"):
			period=a
			print period
		elif o in ("-i","--interval"):
			interval=a
			print interval
		elif o in ("-s","--stop"):
			stop=1
	f=open('./devices.csv','r')
	lines=f.readlines()
#	print lines
	f=open('./server_list.txt','r')
	while True:
		line=f.readline()
		if line and line.find('end')==-1:
			print line.strip()
			print "http://"+line.strip()+":28888"
			server_list.append(xmlrpclib.ServerProxy("http://"+line.strip()+":28888"))
		else:
			f.close()
			break 
	for server in server_list:
		if stop==1:
			print 'stop dev'
			print server.stopDev()
		else:
			print 'start dev'
			print server.startDev(lines,period,interval)
			
		
		
		
		
		
		
		
		