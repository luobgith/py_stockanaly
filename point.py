# -*- coding: utf-8 -*-
import utils

#全局变量True False
release = True

def point(fieldName, candleDict, kdjDict, capitalDict, data):
	ifor = 8
	#fokDif = 
	
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
			print('+++Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)))
			if(release):
				utils.msgTips('Lev5:{0}:{1}'.format(fieldName, utils.objToString(candEn)), 'green')
			return True
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
			
	