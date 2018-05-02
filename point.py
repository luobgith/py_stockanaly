# -*- coding: utf-8 -*-
import utils

def point(fieldName, candleDict, kdjDict, capitalDict, data):
	ifor = 8
	
	can = candleDict[fieldName][-1]
	kdjFil = kdjDict[fieldName][-1]
	#k上十字 入
	if( (abs(can.popen - can.pclose) < 0.03) and ((can.phigh - min(can.pclose,can.popen)) < 0.04) and  (can.phigh - can.plow) / (float(data[1])*0.1) > 0.061 ):
		if(kdjFil.k < 40 and kdjFil.d < 40 and kdjFil.j < 40):
			print('Lev5::'+fieldName+'++++++++++++++++++')
			utils.printObjVal(can)
			print('++++++++++++++++++')
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
			
	#k下十字 出
	if( (abs(can.popen - can.pclose) < 0.03) and ((max(can.pclose,can.popen) - can.plow) < 0.04) and (can.phigh - can.plow) / (float(data[1])*0.1) > 0.061 ):
		if(kdjFil.k > 70 and kdjFil.d > 70 and kdjFil.j > 70):
			print('Lev5::'+fieldName+'------------------')
			utils.printObjVal(can)
			print('------------------')