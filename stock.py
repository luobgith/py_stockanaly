# -*- coding: utf-8 -*-
#类
class CandleEn:
	def __init__(self, popen, pclose, ptime, phigh=0, plow=0, pcounts=0, pmoney=0):
		self.popen = popen
		self.pclose = pclose
		self.ptime = ptime
		self.phigh = phigh
		self.plow = plow
		self.pcounts = pcounts
		self.pmoney = pmoney

#类
class KDJEn:
	def __init__(self, rsv, k=50, d=50, kdjtime='09:00:00'):
		self.rsv = rsv
		self.k = k
		self.d = d
		self.j = 3*k - 2*d
		self.kdjtime = kdjtime

#类
class CapitalEn:
	def __init__(self, ccount, cmoney, inorout, ctime):
		self.ccount = ccount
		self.cmoney = cmoney
		self.inorout = inorout
		self.ctime = ctime
		
"""
蜡烛图: phigh plow popen pclose pcounts pmoney ptime

资金: cmoney ccount inorout ctime

K D J: rsv, k, d, j, kdjtime
以KDJ(9,3,3) 为例:
RSV(9)=（今日收盘价－9日内最低价）÷（9日内最高价－9日内最低价）×100
K(3日)=（当日RSV值+2×前一日K值）÷3
D(3日)=（当日K值+2×前一日D值）÷3
J=3K－2D （这里应该是3k而不是3d）
如果无前一日的K、D值，K、D初始值取50。
"""