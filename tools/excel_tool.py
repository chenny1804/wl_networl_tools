# -*- coding: utf-8 -*- 
import xlwt,xlrd,os,sys
from xlutils.copy import copy

class ExcelList:
	def __init__(self,name):
		self._list_name=name
	
	def CreatList(self):
		wbk = xlwt.Workbook()
		sheet = wbk.add_sheet('sheet 1')
		wbk.save(self._list_name)
	def AddList(self,log):
		i=0
		rb = xlrd.open_workbook(self._list_name)
		wb = copy(rb)
		table = rb.sheets()[0]
		nrows = table.nrows
		sheet = wb.get_sheet(0)
		for field in log.split():
			sheet.write(nrows,i,field)
			i=i+1
			wb.save(self._list_name)
	def PrintList(self):
		data = xlrd.open_workbook(self._list_name)
		table = data.sheets()[0]
		for i in range(table.nrows):
			print table.row_values(i)

excel=ExcelList(sys.argv[1]+'.xls')
excel.CreatList()
for root, dirs, files in os.walk('./'):
	for file in files:
		if file.find(sys.argv[1]+'.txt')!=-1:
			f=open(file,'r')
			while True:
				line=f.readline()
				if line:
					excel.AddList(file.split('_')[0]+' '+line)
				else:
					f.close()
					break 
