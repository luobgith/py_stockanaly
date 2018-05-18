# -*- coding: utf-8 -*-
#类
class CandleEn:
	def __init__(self, name, open, close, date, time, high=0, low=0, volume=0, pmoney=0):
		self.name = name
		self.open = open
		self.close = close
		self.date = date
		self.time = time
		self.high = high
		self.low = low
		self.volume = volume
		self.pmoney = pmoney

#类
class KDJEn:
	def __init__(self, name, rsv, k=50, d=50, date='2018-01-01', time='09:00:00'):
		self.name = name
		self.rsv = rsv
		self.k = k
		self.d = d
		self.j = 3*k - 2*d
		if(self.j > 100):
			self.j = 100
		if(self.j < 0):
			self.j = 0
		self.date = date
		self.time = time

#类
class CapitalEn:
	def __init__(self, name, ccount, cmoney, inorout, date, time):
		self.name = name
		self.ccount = ccount
		self.cmoney = cmoney
		self.inorout = inorout
		self.date = date
		self.time = time
		self.m5 = None
		self.m10 = None

class CaiWuEn:
	def __init__(self, name, code, pe=0, pb=0, BasicEPS=0, NetAssetPerShare=0, mainBusinessIncome=0, IncomeYOYRate=0, retainedProfits=0, ProfitsYOYRate=0, CashFlowPerShare=0, WeightedYieldOnNetAssets=0, SalesGrossMargin=0, totalCapital=0, CirculaValue=0):
		self.name = name
		self.code = code
		self.pe = pe	#市盈率
		self.pb = pb	#市净率
		self.BasicEPS = BasicEPS	#基本每股收益(元)
		self.NetAssetPerShare = NetAssetPerShare	#每股净资产(元)
		self.mainBusinessIncome = mainBusinessIncome	#总营收(万)
		self.IncomeYOYRate = IncomeYOYRate	#营收同比率(%)
		self.retainedProfits = retainedProfits	#净利润(万)
		self.ProfitsYOYRate = ProfitsYOYRate	#净利润同比(%)
		self.CashFlowPerShare = CashFlowPerShare	#每股现金流(元)
		self.WeightedYieldOnNetAssets = WeightedYieldOnNetAssets	#ROE(%)
		self.SalesGrossMargin = SalesGrossMargin	#毛利率(%)
		self.totalCapital = totalCapital	#总市值
		self.CirculaValue = CirculaValue	#流通市值
		
"""
蜡烛图: high low open close volume pmoney ptime

资金: cmoney ccount inorout ctime

K D J: rsv, k, d, j, kdjtime
以KDJ(9,3,3) 为例:
RSV(9)=（今日收盘价－9日内最低价）÷（9日内最高价－9日内最低价）×100
K(3日)=（当日RSV值+2×前一日K值）÷3
D(3日)=（当日K值+2×前一日D值）÷3
J=3K－2D （这里应该是3k而不是3d）
如果无前一日的K、D值，K、D初始值取50。
"""