# -*- coding: utf-8 -*-
import configparser, time, re, requests, csv, pdb, threading
import stock, point, utils
from datetime import datetime

#配置文件变量
conf = configparser.ConfigParser()
conf.read('config.conf')
url = conf.get('net', 'url')
originalDir = conf.get('stock', 'originalDir')
stockPoint = conf.get('stock', 'stockPoint')
dateToday = time.strftime('%Y%m%d')
pattern = re.compile('"(.*)"')

#线程变量
localVal = threading.local()

#全局变量
morningTime = '11:32:00'
afternoonTimeStart = '12:50:00'
afternoonTimeEnd = '15:02:00'
minsDict = {}	#{"min1":1, "min3":3, "min5":5}
for min in conf.get('stock', 'minPoints').split(','):
	minsDict[min] = int(min[-1])

#线程初始化数据
def init_t(stockCode):
	localVal.dataList = []
	localVal.capitalList = []
	localVal.candleDict = {}	##{"min1":[], "min3":[], "min5":[]}
	localVal.kdjDict = {}	##{"min1":[KDJEn(50), ], "min3":[KDJEn(50), ], "min5":[KDJEn(50), ]}
	localVal.capitalDict = {}	###{"min1":[], "min3":[], "min5":[]}
	localVal.stockCode = stockCode
	for min in conf.get('stock', 'minPoints').split(','):
		localVal.candleDict[min] = []
		localVal.kdjDict[min] = [stock.KDJEn(stockCode, 50), ]
		localVal.capitalDict[min] = []

#计算点
def getPoint(timesup):
	for fieldName,mflag in minsDict.items():
		if( timesup.minute % mflag == 0 and len(localVal.dataList) > 2 and (localVal.dataList[-1][31])[0:5] != (localVal.dataList[-2][31])[0:5] ):
			#计算K点
			localVal.candleDict[fieldName].append(utils.candleMin(mflag, timesup, localVal.dataList))
			#计算kdj 9,3,3
			localVal.kdjDict[fieldName].append(utils.kdjCalculate(localVal.candleDict[fieldName], localVal.kdjDict[fieldName]))
			#计算money in or out
			localVal.capitalDict[fieldName].append(utils.capitalMin(mflag, timesup, localVal.capitalList))

			#选点
			point.point(fieldName, localVal.candleDict, localVal.kdjDict, localVal.capitalDict, localVal.dataList[-1])
			
#数据整合 原始数据保存
def analysisdata(contents, stockCode, **kw):
	f = kw.get('f')
	data = pattern.findall(contents.strip())[0].split(',')
	if(len(localVal.dataList) == 0):#第一条
		localVal.capitalList.append( stock.CapitalEn(data[0], int(data[8]), float(data[9]), 0, data[31]) )
		localVal.dataList.append(data)
		if(f):
			f.write(contents)
	else:
		doneDif = int(data[8]) - int(localVal.dataList[-1][8])
		if(doneDif > 0):
			moneyDif = float(data[9])-float(localVal.dataList[-1][9])
			inorout = utils.conpareTowNum(float(data[3]), moneyDif / doneDif)
			localVal.capitalList.append(stock.CapitalEn(data[0], doneDif, moneyDif, inorout, data[31]))
			localVal.dataList.append(data)
			#时间点
			if(stockCode in stockPoint):
				getPoint(datetime.strptime(data[31],'%H:%M:%S'))	#计算点	
			if(f):
				f.write(contents)
				
#读取文件					
def filesStock(filePath, stockCode):
	init_t(stockCode)
	with open(filePath) as f:
		for line in f.readlines():
			#data = pattern.findall(line.strip())[0].split(',')
			analysisdata(line,stockCode)

#网络获取数据
def onlineStock(stockCode):
	init_t(stockCode)
	nowTime = time.strftime('%H:%M:%S')
	with open(originalDir + stockCode + '\\' +stockCode + '-' + dateToday + '.txt', 'a') as f:
		while( (nowTime < morningTime) or ( nowTime < afternoonTimeEnd and nowTime > afternoonTimeStart) ):
			time.sleep(0.5)
			contents = (requests.get(url, params={'list' : stockCode})).text
			analysisdata(contents, stockCode, f=f)
			nowTime = time.strftime('%H:%M:%S')
			
#big 盘
def onlineBigpan(stockCode):
	#headers = ['指数名称','当前点数','当前价格','涨跌率','成交量（手）','成交额（万元）','日期','时间']
	bigpanDataList = []
	nowTime = time.strftime('%H:%M:%S')
	with open(originalDir + stockCode + '\\' +stockCode + '-' + dateToday + '.cvs', 'a', newline='') as f:
		writer = csv.writer(f)
		#writer.writerow(headers)
		while( (nowTime < morningTime) or ( nowTime < afternoonTimeEnd and nowTime > afternoonTimeStart) ):
			time.sleep(5)
			contents = (requests.get(url, params={'list' : stockCode})).text
			data = pattern.findall(contents.strip())[0].split(',')
			data.append(time.strftime('%Y-%m-%d'))
			data.append(time.strftime('%H:%M:%S'))
			if(len(bigpanDataList) == 0):
				bigpanDataList.append(data)
				writer.writerow(data)
			else:
				if(data[4] > bigpanDataList[-1][4]):
					bigpanDataList.append(data)
					writer.writerow(data)
			nowTime = data[7]


	