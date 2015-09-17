# -*- coding:utf-8 -*- 

import sys,os

collect=open('./coolect.csv','w')
collect.write('ID,Caton number,<10,>10,>30,>60\n')
for root, dirs, files in os.walk('./'):
	a_total=0
	a_one_b=0
	a_one_s=0
	a_ten_b=0
	a_six_b=0
	a_thri_b=0
	a_charge=0
	for file in files:
		if file.find('_delay.csv')!=-1:
			total=0
			#print total
			one_b=0
			one_s=0
			ten_b=0
			six_b=0
			thri_b=0
			f=open(file,'r')
			while True:
				line=f.readline()
				if line:
					if line.find('delay time') == -1:
						value=float(line.strip().split(',')[1])
						#print value
						if value > 1000 or value <0.1:
							continue
						else:
							total=total+1
						#	print total
						if value <10:
						#	print '<10'
							one_s=one_s+1
						elif value > 60:
						#	print '>10'
							one_b=one_b+1
							thri_b=thri_b+1
							six_b=six_b+1
							ten_b=ten_b+1
						elif value > 30:
						#	print '>30'
							one_b=one_b+1
							thri_b=thri_b+1
							ten_b=ten_b+1
						elif value > 10:
							one_b=one_b+1
							ten_b=ten_b+1
						elif value > 1:
						#	print '>60'
							one_b=one_b+1
				else:
					f.close()
					break 
	#		print total
			a_total=a_total+total
			a_one_b=a_one_b+one_b
			a_one_s=a_one_s+one_s
			a_ten_b=a_ten_b+ten_b
			a_six_b=a_six_b+six_b
			a_thri_b=a_thri_b+thri_b
			collect.write(file.split('_')[0]+','+str(total)+','+ str(one_s)+ ',' + str(ten_b) + ',' + str(thri_b) + ',' + str(six_b)+'\n')
#	print '3333333333'
	collect.write('TOTAL,'+str(a_total)+','+str(a_one_s)+','+str(a_ten_b)+','+str(a_thri_b)+','+str(a_six_b)+'\n')
	collect.write('percentage,'+ str(float(a_total)/float(a_total)*100) + '%,' +str(float(a_one_s)/float(a_total)*100) +'%,'+ str(float(a_ten_b)/float(a_total)*100)+'%,'+str(float(a_thri_b)/float(a_total)*100)+'%,'+str(float(a_six_b)/float(a_total)*100)+'%\n')
collect.close()