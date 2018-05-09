# -*- coding: utf-8 -*-
import os, threading, time, pdb
from tkinter import *
from datetime import datetime
from matplotlib.pylab import date2num
import matplotlib.pyplot as plt
import matplotlib.mpl_finance as mpf
import stock, handledata

#类的字段名
objAttrTuple = ('high', 'low', 'open', 'close', 'volume', 'pmomey', 'cmoney', 'ccount', 'inorout', 'k', 'd', 'j', 'name', 'kdjdate', 'date', 'time', 'm3', 'm5')
#kdj的两个条件
minKdjCon = 5
maxKdjCon = 10
#量平均线
averas = handledata.maDict

def getDataFilterMin(timeNow,mflag):
	return lambda list: ( timeNow - datetime.strptime(list[31],'%H:%M:%S') ).seconds <= mflag*60
	
def getCapitalFilterMin(timeNow,mflag):
	return lambda cap: ( timeNow - datetime.strptime(cap.time,'%H:%M:%S') ).seconds < mflag*60

#分钟K
def candleMin(mflag, timeNow, dataList):
	if(mflag > 60 or mflag < 0 ):
		raise ValueError('input value must be 0< mflag <60.')
	filtResList = list(filter(getDataFilterMin(timeNow, mflag),dataList[-mflag * 100: ]))
	dataLast = filtResList[-1]
	if(len(filtResList) > 1):
		candle = stock.CandleEn(dataLast[0], float(filtResList[0][3]), float(filtResList[-2][3]), dataLast[30], dataLast[31])
	else:
		candle = stock.CandleEn(dataLast[0], float(filtResList[0][3]), float(filtResList[0][3]), dataLast[30], dataLast[31])
	candle.volume = ( int(filtResList[-1][8]) - int(filtResList[0][8]) )/100
	candle.pmomey = ( float(filtResList[-1][9]) - float(filtResList[0][9]) )/10000
	#排序
	sortList = sorted(filtResList, key=lambda x:x[3])
	candle.high = float(sortList[-1][3])
	candle.low = float(sortList[0][3])
	return candle
	
#kdj
def kdjCalculate(candleList, kdjList):
	kp = 9	#kdj
	lowinkp = float( (sorted(candleList[-kp: ], key=lambda x:x.low))[0].low )
	highinkp = float( (sorted(candleList[-kp: ], key=lambda x:x.high))[-1].high )
	if(highinkp == lowinkp):
		highinkp = highinkp + 0.01
	rsvNow = ( float( candleList[-1].close ) - lowinkp ) / ( highinkp - lowinkp ) * 100
	kvalue = ( rsvNow + 2*kdjList[-1].k ) / 3
	dvalue = ( kvalue + 2*kdjList[-1].d ) / 3
	return stock.KDJEn(candleList[-1].name, rsvNow, kvalue, dvalue, candleList[-1].date, candleList[-1].time)

#zi jing
def capitalMin(mflag, timeNow, capitalList):
	if(mflag > 60 or mflag < 0 ):
		raise ValueError('input value must be 0< mflag <60.')
	filtResList = list(filter(getCapitalFilterMin(timeNow, mflag),capitalList[-mflag * 100: ]))
	ccount, cmoney, inorout = 0,0,0
	for cap in filtResList:
		#ccount += cap.ccount*cap.inorout
		#cmoney += cap.cmoney*cap.inorout
		ccount += cap.ccount
		cmoney += cap.cmoney
	#if(cmoney > 0):
		#inorout = 1
	return stock.CapitalEn(capitalList[-1].name, ccount, cmoney, inorout, capitalList[-1].date, capitalList[-1].time)
	
#平均线3 5
def calAverageCapital(captialList):
	#averas = {'m3':3, 'm5':5}
	captLen = len(captialList)
	#pdb.set_trace()
	if(captLen == 0):
		return False
	for avername, num in averas.items():
		if(captLen < num):
			num = captLen
		calList = captialList[-num: ]
		averaCount = 0
		for cap in calList:
			averaCount += cap.ccount
		setattr(captialList[-1], avername, averaCount/num)
		

#是否满足KDJ超买条件
def buyKdjCondition(kdjList):
	buyCon = 30
	kdjEn = kdjList[-1]
	if(kdjEn.j > buyCon or kdjEn.d > buyCon or kdjEn.k > buyCon):
		return False
	if( abs(kdjEn.j - kdjEn.k) < minKdjCon and abs(kdjEn.k - kdjEn.d) < minKdjCon ):
		return True
	if( abs(kdjEn.j - kdjEn.k) < maxKdjCon and abs(kdjEn.k - kdjEn.d) < maxKdjCon ):
		kdjEnAfter = kdjList[-2]
		if( kdjEn.j - kdjEn.k > 0 and kdjEn.k - kdjEn.d > 0 and kdjEnAfter.j - kdjEnAfter.k < 0 and kdjEnAfter.k - kdjEnAfter.d < 0 ):
			return True
	return False
	
#是否满足KDJ超卖条件
def sellKdjCondition(kdjList):
	sellCon = 70
	kdjEn = kdjList[-1]
	if(kdjEn.j < sellCon or kdjEn.d < sellCon or kdjEn.k < sellCon):
		return False
	if( abs(kdjEn.j - kdjEn.k) < minKdjCon and abs(kdjEn.k - kdjEn.d) < minKdjCon ):
		return True
	if( abs(kdjEn.j - kdjEn.k) < maxKdjCon and abs(kdjEn.k - kdjEn.d) < maxKdjCon ):
		kdjEnAfter = kdjList[-2]
		if( kdjEn.j - kdjEn.k < 0 and kdjEn.k - kdjEn.d < 0 and kdjEnAfter.j - kdjEnAfter.k > 0 and kdjEnAfter.k - kdjEnAfter.d > 0 ):
			return True
	return False
	
#输出类字段及值
def printObjVal(obj):
	for attr in objAttrTuple:
		if( hasattr(obj, attr) ):
			print(attr, '=', getattr(obj, attr), end=' | ')
	print('')
	
#对象转字符串输出
def objToString(obj):
	resStr = ''
	for attr in objAttrTuple:
		if( hasattr(obj, attr) ):
			resStr = resStr + attr + '=' + str(getattr(obj, attr)) + '|'
	return resStr

#获取路径下的所有文件
def getFilesByDir(dirPath, suffix = '.txt'):
	resList = []
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if os.path.splitext(file)[1] == suffix:
				resList.append(os.path.join(root, file))
	return resList
	
#创建文件夹 dirPath：文件夹目录
def mkdir(dirPath):
	dirPath = dirPath.strip().rstrip('\\')	#去除尾部空格和\
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

#比较两数大小,前一个数减后一个数，返回1 0 -1
def conpareTowNum(num1, num2):
	nflag = num1 - num2
	if(nflag > 0):
		return 1
	elif(nflag < 0):
		return -1
	else:
		return 0
		
#新增线程弹出窗体 消息，颜色		
def msgTips(msg, color):
	threading.Thread(target=sendMsgTkinter, args=(msg, color)).start()
	
#线程执行的tk函数
def sendMsgTkinter(msg, color):
	root = Tk()
	text = Text(root, height=3, fg=color)#height=4, width=30,fg=fg
	text.insert(END,msg)
	text.pack()
	root.mainloop()
#============画图=======
#蜡烛
def pltDrawCandle(candleList):
	#mat_wdyx = [[736332.0, 54.01, 54.07, 54.11, 53.711, 30518.0, '002739'],[736333.0, 54.09, 56.691, 56.771, 53.831, 103953.0, '002739'],[736334.0, 56.302, 56.591, 57.08, 55.924, 65414.0, '002739']]
	dataList = []
	for can in candleList:
		#datetime.strptime(can.ptime,'%H:%M:%S')
		detail = []
		"""
		time = 1000*date2num(datetime.strptime(can.date +' '+ can.time,'%Y-%m-%d %H:%M:%S'))
		if(len(dataList) > 0):
			if(time - dataList[-1][0] > 55):
				time = time - 55
		"""
		#time = 1000*date2num(datetime.strptime(can.time,'%H:%M:%S'))
		tmp = can.time.split(':')
		detail.append(int(tmp[0])*100+int(tmp[1]))
		detail.append(can.open)
		detail.append(can.close)
		detail.append(can.high)
		detail.append(can.low)
		detail.append(333)
		detail.append(can.date + can.time)
		dataList.append(detail)
		#print(detail)
	return dataList
	"""
	#pdb.set_trace()
	fig, ax = plt.subplots(figsize=(15,5))
	fig.subplots_adjust(bottom=0.5)
	mpf.candlestick_ochl(ax, dataList, width=0.6, colorup='r', colordown='g', alpha=1.0)
	plt.grid(True)
	# 设置日期刻度旋转的角度
	plt.xticks(rotation=30)
	plt.title('wanda yuanxian 17')
	plt.xlabel('Date')
	plt.ylabel('Price')
	# x轴的刻度为日期
	#ax.xaxis_date()
	plt.show()
	"""

#kdj
def pltDrawKDJ(kdjList, plt):
	x,y1,y2,y3 = [],[],[],[]
	#i = 1
	for kdj in kdjList:
		#x.append(str(i)+kdj.time[0:5])
		#time = 1000*date2num(datetime.strptime(kdj.time,'%H:%M:%S'))
		x.append(kdj.time[0:5])
		y1.append(float(kdj.k))
		y2.append(float(kdj.d))
		y3.append(float(kdj.j))
		#i += 1
		
	#plt.title('k,d,j')	#添加标题
	plt.axis([0, len(x), 0, 100])	#设置边界
	plt.grid(True)	#显示网格
	
	plt.plot(x,y1)
	plt.plot(x,y2)
	plt.plot(x,y3)
	plt.xticks(rotation=90)
	#plt.show()
	
#liang 
def pltDrawCapital(capitalList, plt):
	x, y1, y2, y3 = [], [], [], []
	#i = 1
	for cap in capitalList:
		#x.append(str(i)+cap.time[0:5])
		#time = 1000*date2num(datetime.strptime(cap.time,'%H:%M:%S'))
		x.append(cap.time[0:5])
		#y1.append(cap.cmoney/10000)
		y1.append(cap.ccount/100)
		y2.append(cap.m5/100)
		y3.append(cap.m10/100)
		#i += 1
		#plt.plot([])
	#plt.title('zi jin')	#添加标题
	plt.bar(x,y1,color='g',width =0.3,alpha=0.6)
	#plt.bar(y1,y2,color='g',width = .3,alpha=0.6,label='2015年')
	# 设置日期刻度旋转的角度 
	plt.plot(x,y2)
	plt.plot(x,y3)
	plt.xlim(0, len(x))
	plt.xticks(rotation=90)
	plt.grid(True)
	#plt.show()
	
#3幅图
def pltMultiDraw(**kw):
	candleList = kw.get('candleList')
	kdjList = kw.get('kdjList')
	capitalList = kw.get('capitalList')
	#pdb.set_trace()
	#fig, (ax1,ax2,ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)
	fig, (ax1,ax2,ax3) = plt.subplots(nrows=3, ncols=1)
	fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.14, hspace=0.7)
	plt.sca(ax1)
	plt.grid(True)
	mpf.candlestick_ochl(ax1, pltDrawCandle(candleList), width=0.6, colorup='r', colordown='g', alpha=1.0)
	#plt.xlim(0, 100)
	plt.sca(ax2)
	pltDrawKDJ(kdjList, plt)
	plt.sca(ax3)
	pltDrawCapital(capitalList, plt)
	plt.show()

#####一下为测试函数，未使用
#微信发送消息 不好用
def sengMsgWeixin():
	itchat.auto_login(hotReload=True)
	print(itchat.send('Hello, filehelper', toUserName='filehelper'))
	
if __name__=='__main__':
	mkdir('original\test\123\ ')
		



