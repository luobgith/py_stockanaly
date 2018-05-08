# -*- coding: utf-8 -*-
import configparser, time, re, requests, csv, pdb, threading, os
import stock, point, utils
from datetime import datetime

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

#配置文件变量
conf = configparser.ConfigParser()
conf.read('config.conf', encoding='utf-8-sig')
url = conf.get('net', 'url')
originalDir = conf.get('stock', 'originalDir')
stockPoint = conf.get('stock', 'stockPoint')
pointNames = conf.get('stock', 'pointNames')
dateToday = time.strftime('%Y%m%d')
pattern = re.compile('"(.*)"')

#线程变量
localVal = threading.local()	#未使用

#全局变量
timeStart = '09:15:00'
timeEnd = '15:02:00'
minsDict = {}	#{"min1":1, "min3":3, "min5":5}
candleDict = {}	##{"min1":[], "min3":[], "min5":[]}
kdjDict = {}	##{"min1":[KDJEn(50), ], "min3":[KDJEn(50), ], "min5":[KDJEn(50), ]}
capitalDict = {}	###{"min1":[], "min3":[], "min5":[]}
for min in conf.get('stock', 'minPoints').split(','):
	minsDict[min] = int(min[-1])
	candleDict[min] = []
	kdjDict[min] = [stock.KDJEn('', 50), ]
	capitalDict[min] = []
"""	
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

#数据初始化
def init_d(stockCode):
	fileList = utils.getFilesByDir(originalDir + stockCode)
	if (len(fileList) > 0):
		for filePath in fileList[-3: ]:
			print(filePath)
			with open(filePath) as f:
				for line in f.readlines():
					analysisdata(line,stockCode)
				localVal.dataList = []
				localVal.capitalList = []
				
#数据初始化 读取文件分析使用
def init_d_file(stockCode):
	fileList = utils.getFilesByDir(originalDir + stockCode)
	if (len(fileList) > 0):
		for filePath in fileList[-4:-1]:
			print(filePath)
			with open(filePath) as f:
				for line in f.readlines():
					analysisdata(line,stockCode)
				localVal.dataList = []
				localVal.capitalList = []

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
		if(stockCode in stockPoint):
			localVal.capitalList.append( stock.CapitalEn(data[0], int(data[8]), float(data[9]), 0, data[31]) )
			localVal.dataList.append(data)
		if(f):
			f.write(contents)
	else:
		doneDif = int(data[8]) - int(localVal.dataList[-1][8])
		if(doneDif > 0):
			#需要监控的stock
			if(stockCode in stockPoint):
				moneyDif = float(data[9])-float(localVal.dataList[-1][9])
				inorout = utils.conpareTowNum(float(data[3]), moneyDif / doneDif)
				localVal.capitalList.append(stock.CapitalEn(data[0], doneDif, moneyDif, inorout, data[31]))
				localVal.dataList.append(data)
				getPoint(datetime.strptime(data[31],'%H:%M:%S'))	#计算点	
			if(f):
				f.write(contents)
				
#读取文件					
def filesStock(filePath, stockCode):
	init_t(stockCode)
	if(stockCode in stockPoint):
		init_d_file(stockCode)
	with open(filePath) as f:
		for line in f.readlines():
			analysisdata(line,stockCode)
"""
#======第二版
countFlag = 1	#全局计数变量
origiDict = {}
capitalOrigiDict = {}
def init_origi():
	global countFlag
	for stockName in conf.get('stock', 'stockNames').split(','):
		origiDict[stockName] = []
		capitalOrigiDict[stockName] = []
		countFlag = 1

#初始化 读取历史数据
def init_h():
	init_origi()
	fileList = utils.getFilesByDir(originalDir + os.sep + 'stock', suffix = '.cvs')
	if(len(fileList) == 0 ):
		return False
	for fieldName,mflag in minsDict.items():
		for filePath in fileList[-mflag-1: ]:
			with open(filePath) as f:
				reader = csv.reader(f)
				for data in reader:
					dealOrigeData(data)
					if(data[0] in pointNames):
						analysisOrgiData(data[0], fieldName = fieldName)
				"""
					stockName = data[0]
					origiList = origiDict[stockName]
					#capitalList = capitalOrigiDict[stockName]
					if(len(origiList) == 0 ):
						origiDict[stockName].append(data)
						capitalOrigiDict[stockName].append( stock.CapitalEn(data[0], int(data[8]), float(data[9]), 0, data[31]) )
					else:
						doneDif = int(data[8]) - int(origiList[-1][8])
						if(doneDif > 0):
							moneyDif = float(data[9])-float(origiList[-1][9])
							inorout = utils.conpareTowNum(float(data[3]), moneyDif / doneDif)
							capitalOrigiDict[stockName].append(stock.CapitalEn(data[0], doneDif, moneyDif, inorout, data[31]))
							origiDict[stockName].append(data)
				"""
					
			init_origi()

#处理原始数据
def dealOrigeData(data, **kw):
	#pdb.set_trace()
	stockName = data[0]
	writer = kw.get('writer')
	origiList = origiDict[stockName]
	#capitalList = capitalOrigiDict[stockName]
	if(len(origiList) == 0 ):
		origiDict[stockName].append(data)
		capitalOrigiDict[stockName].append( stock.CapitalEn(data[0], int(data[8]), float(data[9]), 0, data[30], data[31]) )
		if(writer):
			writer.writerow(data)
	else:
		doneDif = int(data[8]) - int(origiList[-1][8])
		if(doneDif > 0):
			moneyDif = float(data[9])-float(origiList[-1][9])
			inorout = utils.conpareTowNum(float(data[3]), moneyDif / doneDif)
			capitalOrigiDict[stockName].append(stock.CapitalEn(data[0], doneDif, moneyDif, inorout, data[30], data[31]))
			origiDict[stockName].append(data)
			if(writer):
				writer.writerow(data)

#网络获取数据
def onlineStock():
	init_h()
	nowTime = time.strftime('%H:%M:%S')
	#for tmp in capitalDict['min5']:
		#print(utils.objToString(tmp))
	with open(originalDir + os.sep + 'stock' + os.sep + dateToday + '-stock.cvs', 'a', newline='') as f:
		writer = csv.writer(f)
		while( (nowTime > timeStart) and ( nowTime < timeEnd ) ):
			
			time.sleep(1.5)
			contentList = pattern.findall((requests.get(url+'?list='+conf.get('stock', 'stockCodes'))).text)
			for line in contentList:
				#pdb.set_trace()
				data = line.split(',')
				dealOrigeData(data, writer = writer)
				if(data[0] in pointNames):
					analysisOrgiData(data[0])
			nowTime = time.strftime('%H:%M:%S')
			"""
				data = line.split(',')
				stockName = data[0]
				origiList = origiDict[stockName]
				#capitalList = capitalOrigiDict[stockName]
				if(len(origiList) == 0 ):
					origiDict[stockName].append(data)
					capitalOrigiDict[stockName].append( stock.CapitalEn(data[0], int(data[8]), float(data[9]), 0, data[31]) )
					writer.writerow(data)
				else:
					doneDif = int(data[8]) - int(origiList[-1][8])
					if(doneDif > 0):
						moneyDif = float(data[9])-float(origiList[-1][9])
						inorout = utils.conpareTowNum(float(data[3]), moneyDif / doneDif)
						capitalOrigiDict[stockName].append(stock.CapitalEn(data[0], doneDif, moneyDif, inorout, data[31]))
						origiDict[stockName].append(data)
						writer.writerow(data)
			"""
				
#数据计算
def analysisOrgiData(pointName, **kw):
	global countFlag
	if(len(origiDict[pointName]) > countFlag):
		countFlag += 1
		origiList = origiDict[pointName][0:countFlag]
		timesup = datetime.strptime(origiList[-1][31],'%H:%M:%S')
		fieldName = kw.get('fieldName')
		if(fieldName):
			mflag = minsDict[fieldName]
			if( timesup.minute % mflag == 0 and (origiList[-1][31])[0:5] != (origiList[-2][31])[0:5] ):
				candleDict[fieldName].append(utils.candleMin(mflag, timesup, origiList))
				kdjDict[fieldName].append(utils.kdjCalculate(candleDict[fieldName], kdjDict[fieldName]))
				capitalDict[fieldName].append(utils.capitalMin(mflag, timesup, capitalOrigiDict[pointName]))
		else:
			for fieldName,mflag in minsDict.items():
				if( timesup.minute % mflag == 0 and (origiList[-1][31])[0:5] != (origiList[-2][31])[0:5] ):
					#蜡烛点
					candleDict[fieldName].append(utils.candleMin(mflag, timesup, origiList))
					#kdj 9,3,3
					kdjDict[fieldName].append(utils.kdjCalculate(candleDict[fieldName], kdjDict[fieldName]))
					#money in or out
					capitalDict[fieldName].append(utils.capitalMin(mflag, timesup, capitalOrigiDict[pointName]))
					#print('{0}:{1}--{2}--{3}'.format(fieldName, utils.objToString(candleDict[fieldName][-1]), len(origiList), countFlag))
					#选点
					point.point(fieldName, candleDict, kdjDict, capitalDict, origiList[-1])

"""
#网络获取数据
def onlineStock(stockCode):
	init_t(stockCode)
	if(stockCode in stockPoint):
		init_d(stockCode)
	nowTime = time.strftime('%H:%M:%S')
	utils.mkdir(originalDir + stockCode)	#目录不存在则创建
	with open(originalDir + stockCode + os.sep +stockCode + '-' + dateToday + '.txt', 'a') as f:
		#while( (nowTime < morningTime) or ( nowTime < timeEnd and nowTime > afternoonTimeStart) ):
		while( (nowTime > timeStart) and ( nowTime < timeEnd ) ):
			time.sleep(1.5)
			contents = (requests.get(url, params={'list' : stockCode})).text
			analysisdata(contents, stockCode, f=f)
			nowTime = time.strftime('%H:%M:%S')
"""	
		
#big 盘
def onlineBigpan(stockCode):
	#headers = ['指数名称','当前点数','当前价格','涨跌率','成交量（手）','成交额（万元）','日期','时间']
	bigpanDataList = []
	nowTime = time.strftime('%H:%M:%S')
	with open(originalDir + stockCode + os.sep +stockCode + '-' + dateToday + '.cvs', 'a', newline='') as f:
		writer = csv.writer(f)
		while( (nowTime > timeStart) and ( nowTime < timeEnd ) ):
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
			
#通过日期选择数据
def filterdate(x):
	dateNow = '2018-05-08'
	return x.date == dateNow
			
if __name__=='__main__':
	#dateNow = '2018-05-08'
	init_h()
	utils.pltMultiDraw(candleList = filter(filterdate, candleDict['min5']), kdjList = filter(filterdate, kdjDict['min5']), capitalList = filter(filterdate, capitalDict['min5']))
	utils.pltMultiDraw(candleList = filter(filterdate, candleDict['min3']), kdjList = filter(filterdate, kdjDict['min3']), capitalList = filter(filterdate, capitalDict['min3']))
	utils.pltMultiDraw(candleList = filter(filterdate, candleDict['min1']), kdjList = filter(filterdate, kdjDict['min1']), capitalList = filter(filterdate, capitalDict['min1']))
	#utils.pltDrawCandle(filter(lambda x : x.date == dateNow , candleDict['min5']))
	#utils.pltDrawKDJ(filter(lambda x : x.date == dateNow , kdjDict['min5']))
	#pdb.set_trace()
	#utils.pltDrawCapital(filter(lambda x : x.date == dateNow , capitalDict['min5']))
	