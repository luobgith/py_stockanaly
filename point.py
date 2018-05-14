# -*- coding: utf-8 -*-
import utils

#全局变量True False
release = True
#成交量固定指标
volumeFlag = 100000
volumeFlagTotal = 250000
"""
volumeStand = {'浪潮信息':{'min5':0.00009, 'min3':0.0008}, '赣锋锂业':{'min5':0.0005, 'min3':0.0008}}
#baseVal = 100000000
cflag5 = None
cflag3 = None
#初始化基本数据
def init(name):
	global cflag5
	global cflag3
	cflag5 = volumeStand[name][0]
	cflag3 = volumeStand[name][1]
"""
def point(fieldName, candleDict, kdjDict, capitalDict, data):
	#ifor = 8
	candEn = candleDict[fieldName][-1]
	kdjEn = kdjDict[fieldName][-1]
	capEn = capitalDict[fieldName][-1]
	#k上十字 入 5级
	if( (abs(candEn.open - candEn.close) < 0.03) and ((candEn.high - min(candEn.close,candEn.open)) < 0.04) and  (candEn.high - candEn.low) / (float(data[1])*0.1) > 0.061 ):
		if(kdjEn.k < 30 and kdjEn.d < 30 and kdjEn.j < 30):
			print('+++Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)))
			if(release):
				utils.msgTips('Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)), 'red')
			return True
	#k下十字 出 5级
	if( (abs(candEn.open - candEn.close) < 0.03) and ((max(candEn.close,candEn.open) - candEn.low) < 0.04) and (candEn.high - candEn.low) / (float(data[1])*0.1) > 0.061 ):
		if(kdjEn.k > 70 and kdjEn.d > 70 and kdjEn.j > 70):
			print('---Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)))
			if(release):
				utils.msgTips('Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)), 'green')
			return True
	
	#5min 3min 同时超买
	if(utils.buyKdjCondition(kdjDict[fieldName])):	#如果满足超卖
		str = 'Lev2:{0}:{1}:price={2}'.format(fieldName, utils.objToString(kdjEn), candEn.close)
		if(fieldName == 'min3'):	#如果是3分钟
			if(utils.buyKdjCondition(kdjDict['min5'])): #则看5分钟的第一个是否满足
				print('+++'+str)
				if(release):
					utils.msgTips(str, 'red')
		elif(fieldName == 'min5'):	#如果是5分钟
			if(utils.buyKdjCondition(kdjDict['min3'])): #则看3分钟的第一个是否满足
				print('+++'+str)
				if(release):
					utils.msgTips(str, 'red')
			elif(utils.buyKdjCondition(kdjDict['min3'][0:(len(kdjDict['min3'])-1)])): #则看3分钟的第二个是否满足
				print('+++'+str)
				if(release):
					utils.msgTips(str, 'red')
					
	#成交量 出 
	if(kdjEn.k > 75 and kdjEn.d > 70 and kdjEn.j > 80):
		str = 'Lev4:{0}:{1}:price={2}'.format(fieldName, utils.objToString(kdjEn), candEn.close)
		capEn2 = capitalDict[fieldName][-2]
		capEn3 = capitalDict[fieldName][-3]
		#5下交10
		if(capEn.m5 - capEn2.m5 < -volumeFlag):
			if(abs(capEn.m5 - capEn.m10)/capEn.m5 < 0.01):
				print('---'+str)
				if(release):
					utils.msgTips(str, 'green')
			elif( capEn.m5 - capEn.m10 < 0 and capEn2.m5 - capEn2.m10 > 0 ):
				print('---'+str)
				if(release):
					utils.msgTips(str, 'green')
			elif( capEn2.m5 - capEn3.m5 > 0 and abs(capEn2.m5 - capEn3.m5) + abs(capEn.m5 - capEn2.m5) > volumeFlagTotal):	##正负夹角
				print('---'+str)
				if(release):
					utils.msgTips(str, 'green')
		#正负夹角
		if( capEn3.m5 - capEn.m5 < -(2*volumeFlag) and abs(capEn3.m5 - capEn.m5) + (capitalDict[fieldName][-3] - capitalDict[fieldName][-5]) > 2*volumeFlagTotal ):
			print('---'+str)
				if(release):
					utils.msgTips(str, 'green')
		
	#看数据用
	#if(fieldName == 'min5'):
		#print('{0}:{1}'.format(fieldName, utils.objToString(capEn)))
	"""		
	#超买 以KDJ为基础再添加其他指标
	if(utils.buyKdjCondition(kdjDict[fieldName])):
		#三个蜡烛中有十字星
		if( len( list( filter( lambda x: abs(x.close - x.open) < 0.03, candleDict[fieldName][-3: ] ) ) ) > 0  ):
			print('+++Lev1:{0}:{1}'.format(fieldName, utils.objToString(kdjEn)))
		
	
	#超卖 以KDJ为基础再添加其他指标
	if(utils.sellKdjCondition(kdjDict[fieldName])):
		#三个蜡烛中有十字星
		if( len( list( filter( lambda x: abs(x.close - x.open) < 0.03, candleDict[fieldName][-3: ] ) ) ) > 0  ):
			print('---Lev1:{0}:{1}'.format(fieldName, utils.objToString(kdjEn)))
	"""
	
	