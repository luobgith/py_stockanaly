# -*- coding: utf-8 -*-
import os, threading, time
from tkinter import *
from datetime import datetime
import stock

#类的字段名
objAttrTuple = ('phigh', 'plow', 'popen', 'pclose', 'pcounts', 'pmomey', 'ptime', 'cmoney', 'ccount', 'inorout', 'ctime', 'k', 'd', 'j', 'kdjtime', 'name')
#kdj的两个条件
minKdjCon = 5
maxKdjCon = 10

def getDataFilterMin(timeNow,mflag):
	return lambda list: ( timeNow - datetime.strptime(list[31],'%H:%M:%S') ).seconds <= mflag*60
	
def getCapitalFilterMin(timeNow,mflag):
	return lambda cap: ( timeNow - datetime.strptime(cap.ctime,'%H:%M:%S') ).seconds < mflag*60

#分钟K
def candleMin(mflag, timeNow, dataList):
	if(mflag > 60 or mflag < 0 ):
		raise ValueError('input value must be 0< mflag <60.')
	filtResList = list(filter(getDataFilterMin(timeNow, mflag),dataList[-mflag * 100: ]))
	dataLast = filtResList[-1]
	if(len(filtResList) > 1):
		candle = stock.CandleEn(dataLast[0], float(filtResList[0][3]), float(filtResList[-2][3]), dataLast[31])
	else:
		candle = stock.CandleEn(dataLast[0], float(filtResList[0][3]), float(filtResList[0][3]), dataLast[31])
	candle.pcounts = ( int(filtResList[-1][8]) - int(filtResList[0][8]) )/100
	candle.pmomey = ( float(filtResList[-1][9]) - float(filtResList[0][9]) )/10000
	#排序
	sortList = sorted(filtResList, key=lambda x:x[3])
	candle.phigh = float(sortList[-1][3])
	candle.plow = float(sortList[0][3])
	return candle
	
#kdj
def kdjCalculate(candleList, kdjList):
	kp = 9	#kdj
	lowinkp = float( (sorted(candleList[-kp: ], key=lambda x:x.plow))[0].plow )
	highinkp = float( (sorted(candleList[-kp: ], key=lambda x:x.phigh))[-1].phigh )
	if(highinkp == lowinkp):
		highinkp = highinkp + 0.01
	rsvNow = ( float( candleList[-1].pclose ) - lowinkp ) / ( highinkp - lowinkp ) * 100
	kvalue = ( rsvNow + 2*kdjList[-1].k ) / 3
	dvalue = ( kvalue + 2*kdjList[-1].d ) / 3
	return stock.KDJEn(candleList[-1].name, rsvNow, kvalue, dvalue, candleList[-1].ptime)

#zi jing
def capitalMin(mflag, timeNow, capitalList):
	if(mflag > 60 or mflag < 0 ):
		raise ValueError('input value must be 0< mflag <60.')
	filtResList = list(filter(getCapitalFilterMin(timeNow, mflag),capitalList[-mflag * 100: ]))
	ccount, cmoney, inorout = 0,0,-1
	for cap in filtResList:
		ccount += cap.ccount*cap.inorout
		cmoney += cap.cmoney*cap.inorout
	if(cmoney > 0):
		inorout = 1
	return stock.CapitalEn(capitalList[-1].name, ccount, cmoney, inorout, capitalList[-1].ctime)

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
	
#输出类字段及值（需要把字段配在这里）
def printObjVal(obj):
	#objAttrTuple = ('name', 'phigh', 'plow', 'popen', 'pclose', 'pcounts', 'pmomey', 'ptime', 'cmoney', 'ccount', 'inorout', 'ctime', 'k', 'd', 'j', 'kdjtime')
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

#####一下为测试函数，未使用
#微信发送消息 不好用
def sengMsgWeixin():
	itchat.auto_login(hotReload=True)
	print(itchat.send('Hello, filehelper', toUserName='filehelper'))
	
if __name__=='__main__':
	tmp = 1
	if(tmp):
		print('123')
		



