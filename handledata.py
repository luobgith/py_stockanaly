# -*- coding: utf-8 -*-
import configparser, time, re, requests, csv, pdb
import stock, point, utils
from datetime import datetime

conf = configparser.ConfigParser()
conf.read('config.conf')

url = conf.get('net', 'url')
originalDir = conf.get('stock', 'originalDir')
dateToday = time.strftime('%Y%m%d')
pattern = re.compile('"(.*)"')

#初始化数据
minsDict = {}	#{"min1":1, "min3":3, "min5":5}
candleDict = {}	#{"min1":[], "min3":[], "min5":[]}
kdjDict = {}	#{"min1":[KDJEn(50), ], "min3":[KDJEn(50), ], "min5":[KDJEn(50), ]}
capitalDict = {}	#{"min1":[], "min3":[], "min5":[]}
dataList = []
capitalList = []

#初始化数据
def init():
	#pdb.set_trace()
	global dataList
	global capitalList
	dataList = []
	capitalList = []
	for min in conf.get('stock', 'minPoints').split(','):
		minsDict[min] = int(min[-1])
		candleDict[min] = []
		kdjDict[min] = [stock.KDJEn(50), ]
		capitalDict[min] = []

def analysisdata(contents):
	#pdb.set_trace()
	data = pattern.findall(contents.strip())[0].split(',')
	if(len(dataList) == 0):#第一条
		capitalList.append( stock.CapitalEn(int(data[8]), float(data[9]), 0, data[31]) )
		dataList.append(data)
		#f.write(contents)
	else:
		#if(data[30] != dataList[-1][30]):#第二天的数据
			#dataList = []
			#dataList.append(data)
			#print(data[30],'===',dataList[-1])
		doneDif = int(data[8]) - int(dataList[-1][8])
		if(doneDif > 0):
			moneyDif = float(data[9])-float(dataList[-1][9])
			junjia = moneyDif / doneDif
			if(junjia > float(data[3])):
				inorout = -1
			elif(junjia < float(data[3])):
				inorout = 1
			else:
				inorout = 0
			capitalList.append(stock.CapitalEn(doneDif, moneyDif, inorout, data[31]))
			dataList.append(data)
			#时间点
			timesup = datetime.strptime(data[31],'%H:%M:%S')
			for fieldName,mflag in minsDict.items():
				if( timesup.minute % mflag == 0 and len(dataList) > 2 and data[31][0:5] != (dataList[-2][31])[0:5] ):
					#计算K点
					candleDict[fieldName].append(utils.candleMin(mflag, timesup, dataList))
					#计算kdj 9,3,3
					kdjDict[fieldName].append(utils.kdjCalculate(candleDict[fieldName], kdjDict[fieldName]))
					#计算money in or out
					capitalDict[fieldName].append(utils.capitalMin(mflag, timesup, capitalList))
	
					#选点
					point.point(fieldName, candleDict, kdjDict, capitalDict, data)
			
			#f.write(contents)

def handleStock(stockID):
	nowTime = '09:00:00'
	with open(originalDir + stockID + '\\' +stockID + '-' + dateToday + '.txt', 'a') as f:
		while(nowTime < "15:01:00"):
			time.sleep(0.5)
			contents = (requests.get(url, params={'list' : stockID})).text
			data = pattern.findall(contents.strip())[0].split(',')
			if(len(dataList) == 0):#第一条
				capitalList.append( stock.CapitalEn(int(data[8]), float(data[9]), 0, data[31]) )
				dataList.append(data)
				f.write(contents)
			else:
				doneDif = int(data[8]) - int(dataList[-1][8])
				if(doneDif > 0):
					moneyDif = float(data[9])-float(dataList[-1][9])
					junjia = moneyDif / doneDif
					if(junjia > float(data[3])):
						inorout = -1
					elif(junjia < float(data[3])):
						inorout = 1
					else:
						inorout = 0
					capitalList.append(stock.CapitalEn(doneDif, moneyDif, inorout, data[31]))
					dataList.append(data)
					#时间点
					timesup = datetime.strptime(data[31],'%H:%M:%S')
					for fieldName,mflag in minsDict.items():
						if( timesup.minute % mflag == 0 and len(dataList) > 2 and data[31][0:5] != (dataList[-2][31])[0:5] ):
							#计算K点
							candleDict[fieldName].append(utils.candleMin(mflag, timesup, dataList))
							#计算kdj 9,3,3
							kdjDict[fieldName].append(utils.kdjCalculate(candleDict[fieldName], kdjDict[fieldName]))
							#计算money in or out
							capitalDict[fieldName].append(utils.capitalMin(mflag, timesup, capitalList))
			
							#选点
							point.point(fieldName, candleDict, kdjDict, capitalDict, data)
					
					f.write(contents)
			nowTime = time.strftime('%H:%M:%S')

def bigPanData(code):
	headers = ['指数名称','当前点数','当前价格','涨跌率','成交量（手）','成交额（万元）','日期','时间']
	dataList = []
	nowTime = '09:00:00'
	with open(originalDir + code + '\\' +code + '-' + dateToday + '.cvs', 'w', newline='') as f:
		#writer = csv.DictWriter(f, headers)
		writer = csv.writer(f)
		writer.writerow(headers)
		#writer.writeheader()
		while(nowTime < "15:01:00"):
			time.sleep(5)
			contents = (requests.get(url, params={'list' : code})).text
			data = pattern.findall(contents.strip())[0].split(',')
			data.append(time.strftime('%Y-%m-%d'))
			data.append(time.strftime('%H:%M:%S'))
			print(data)
			writer.writerow(data)
			
			nowTime = data[-1]


	