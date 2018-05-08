# -*- coding: utf-8 -*-
import utils

#全局变量True False
release = True

def point(fieldName, candleDict, kdjDict, capitalDict, data):
	#ifor = 8
	candEn = candleDict[fieldName][-1]
	kdjFil = kdjDict[fieldName][-1]
	#k上十字 入 5级
	if( (abs(candEn.popen - candEn.pclose) < 0.03) and ((candEn.phigh - min(candEn.pclose,candEn.popen)) < 0.04) and  (candEn.phigh - candEn.plow) / (float(data[1])*0.1) > 0.061 ):
		if(kdjFil.k < 30 and kdjFil.d < 30 and kdjFil.j < 30):
			print('+++Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)))
			if(release):
				utils.msgTips('Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)), 'red')
			return True
	#k下十字 出 5级
	if( (abs(candEn.popen - candEn.pclose) < 0.03) and ((max(candEn.pclose,candEn.popen) - candEn.plow) < 0.04) and (candEn.phigh - candEn.plow) / (float(data[1])*0.1) > 0.061 ):
		if(kdjFil.k > 70 and kdjFil.d > 70 and kdjFil.j > 70):
			print('---Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)))
			if(release):
				utils.msgTips('Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)), 'green')
			return True
	
	#5min 3min 同时超买
	if(utils.buyKdjCondition(kdjDict[fieldName])):	#如果满足超卖
		if(fieldName == 'min3'):	#如果是3分钟
			if(utils.buyKdjCondition(kdjDict['min5'])): #则看5分钟的第一个是否满足
				print('+++Lev2:{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
		elif(fieldName == 'min5'):	#如果是5分钟
			if(utils.buyKdjCondition(kdjDict['min3'])): #则看3分钟的第一个是否满足
				print('+++Lev2:{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
			elif(utils.buyKdjCondition(kdjDict['min3'][0:(len(kdjDict['min3'])-1)])): #则看3分钟的第二个是否满足
				print('+++Lev2:{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
				
	#看数据用
	if(fieldName == 'min5'):
		print('{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
	"""		
	#超买 以KDJ为基础再添加其他指标
	if(utils.buyKdjCondition(kdjDict[fieldName])):
		#三个蜡烛中有十字星
		if( len( list( filter( lambda x: abs(x.pclose - x.popen) < 0.03, candleDict[fieldName][-3: ] ) ) ) > 0  ):
			print('+++Lev1:{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
		
	
	#超卖 以KDJ为基础再添加其他指标
	if(utils.sellKdjCondition(kdjDict[fieldName])):
		#三个蜡烛中有十字星
		if( len( list( filter( lambda x: abs(x.pclose - x.popen) < 0.03, candleDict[fieldName][-3: ] ) ) ) > 0  ):
			print('---Lev1:{0}:{1}'.format(fieldName, utils.objToString(kdjFil)))
	"""
	
	"""
	#KDJ 入
	if( abs(kdjFil.j - kdjFil.d) < ifor and  abs(kdjFil.d - kdjFil.k) < ifor ):
		for kdjfor in kdjDict[fieldName][-ifor: ]:
			if( kdjfor.k < 30 and kdjfor.d < 30 and kdjfor.j < 30 ):
				ifor -= 1
		if(ifor == 0):
			print('Lev1::'+fieldName+'++++++++++++++++++')
			utils.printObjVal(kdjFil)
			print('++++++++++++++++++')
	
	#kdj 出
	if( abs(kdjFil.j - kdjFil.d) < ifor and  abs(kdjFil.d - kdjFil.k) < ifor ):
		for kdjfor in kdjDict[fieldName][-ifor: ]:
			if( kdjfor.k > 60 and kdjfor.d > 60 and kdjfor.j > 60 ):
				ifor -= 1
		if(ifor == 0):
			print('Lev1::'+fieldName+'------------------')
			utils.printObjVal(kdjFil)
			print('------------------')
	"""		
	