# -*- coding: utf-8 -*-
import stock
from datetime import datetime

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
		candle = stock.CandleEn(float(filtResList[0][3]), float(filtResList[-2][3]), dataLast[31])
	else:
		candle = stock.CandleEn(float(filtResList[0][3]), float(filtResList[0][3]), dataLast[31])
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
	return stock.KDJEn(rsvNow, kvalue, dvalue, candleList[-1].ptime)

#zi jing
def capitalMin(mflag, timeNow, capitalList):
	if(mflag > 60 or mflag < 0 ):
		raise ValueError('input value must be 0< mflag <60.')
	#pdb.set_trace()
	filtResList = list(filter(getCapitalFilterMin(timeNow, mflag),capitalList[-mflag * 100: ]))
	ccount, cmoney, inorout = 0,0,-1
	for cap in filtResList:
		ccount += cap.ccount*cap.inorout
		cmoney += cap.cmoney*cap.inorout
	if(cmoney > 0):
		inorout = 1
	return stock.CapitalEn(ccount, cmoney, inorout, capitalList[-1].ctime)