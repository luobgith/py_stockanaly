# -*- coding: utf-8 -*-
import utils

def point(fieldName, candleDict, kdjDict, capitalDict, data):
	can = candleDict[fieldName][-1]
	kdjFil = kdjDict[fieldName][-1]
	#k上十字 入
	if( (abs(can.popen - can.pclose) < 0.03) and ((can.phigh - min(can.pclose,can.popen)) < 0.04) and  (can.phigh - can.plow) / (float(data[1])*0.1) > 0.065 ):
		if(kdjFil.k < 50 and kdjFil.d < 50 and kdjFil.j < 50):
			print('++++++++++++++++++')
			utils.printObjVal(can)
			print('++++++++++++++++++')
	#kdj 出
	ifor = 8	#往前几个推是>0 的
	if( abs(kdjFil.j - kdjFil.d) < ifor and  abs(kdjFil.d - kdjFil.k) < ifor ):
		for kdjfor in kdjDict[fieldName][-ifor: ]:
			if( kdjfor.k > 60 and kdjfor.d > 60 and kdjfor.j > 60 ):
				ifor -= 1
		if(ifor == 0):
			print('------------------')
			utils.printObjVal(kdjFil)
			print('------------------')