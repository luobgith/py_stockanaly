# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.mpl_finance as mpf
from matplotlib.pylab import date2num
import requests, csv, re, time, json
import stock, utils, config

requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

#kdj
def pltDrawKDJ(kdjList):
	fig, ax = plt.subplots()
	x,y1,y2,y3 = [],[],[],[]
	for kdj in kdjList:
		#x.append(date2num(datetime.strptime(kdj.date,'%Y-%m-%d')))
		x.append(kdj.date)
		y1.append(float(kdj.k))
		y2.append(float(kdj.d))
		y3.append(float(kdj.j))
	plt.axis([0, len(x), 0, 100])	#设置边界
	plt.grid(True)	#显示网格
	plt.plot(x,y1)
	plt.plot(x,y2)
	plt.plot(x,y3)
	plt.xticks(rotation=90)
	plt.show()
	
#candle
def pltDrawCandle2(candleList):
	reCandleList = []
	for can in candleList:
		detail = []
		detail.append(date2num(datetime.strptime(can.date,'%Y-%m-%d')))
		detail.append(can.open)
		detail.append(can.close)
		detail.append(can.high)
		detail.append(can.low)
		detail.append(can.volume)
		detail.append(can.name)
		reCandleList.append(detail)
	fig, ax = plt.subplots()
	plt.grid(True)
	mpf.candlestick_ochl(ax,reCandleList, width=0.6, colorup='r', colordown='g', alpha=1.0)
	plt.xticks(rotation=90)
	ax.xaxis_date()
	plt.show()

#抓取网页代码函数
def getStackCode(html):
	s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
	pat = re.compile(s)
	code = pat.findall(html)
	return code

urlCode = 'http://quote.eastmoney.com/stocklist.html'
urlHistory = 'http://quotes.money.163.com/service/chddata.html?code={0}{1}&start={2}'
pattern = re.compile('\((.*)\)')
urlzc = 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id={0}{1}'
urlcwzy = 'http://data.eastmoney.com/DataCenter_V3/stockdata/cwzy.ashx?code={0}.{1}'

def catchStockCaiWu(code):
	codeFalg1 = '2'
	if(code[0] == '6'):
		codeFalg1 = '1'
	codeFalg2 = 'SZ'
	if(code[0] == '6'):
		codeFalg2 = 'SH'
	zc = json.loads(pattern.findall(requests.get(urlzc.format(code, codeFalg1)).text)[0])['Value']
	#print(zc)
	if(len(zc) < 1):
		return None
	peValue = -1000
	pbValue = -1000
	try:
		peValue = float(zc[38])
		pbValue = float(zc[43])
	except ValueError as e:
		pass
	caiWu = stock.CaiWuEn(zc[2], code, CirculaValue=float(zc[45]), totalCapital=float(zc[46]), pe=peValue, pb=pbValue)
	#cwzy = json.loads(requests.get(urlcwzy.format(code, codeFalg2)).text)[0]
	cwzy = (requests.get(urlcwzy.format(code, codeFalg2)).json())[0]
	for attr in config.objAttrTuple:
		if(attr in cwzy):
			value = -1000
			try:
				value = float(cwzy[attr])
			except ValueError as e:
				#print(value)
				pass
			setattr(caiWu, attr, value)
	return caiWu
	"""
	with open('cw.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(tmp['Value'])
	"""
	#utils.printObjVal(caiWu)
	
def main_func():
	codes = getStackCode(requests.get(urlCode).text)
	codeList = []
	for item in codes:
		if(item[0:2]=='60' or item[0:2]=='00'):
			codeList.append(item)

	dayStart = (datetime.now() - timedelta(days=200)).strftime('%Y%m%d')
	#读取文件
	passCodes = []
	with open('passcode.txt', 'r') as f:
		passCodes = f.read()
		#passCodes = text.split(',')
		
	with open('passcode.txt', 'a') as f:
		#for code in codeList[-1500: ]:
		for code in codeList:
			#base case
			if(code in passCodes):
				continue
			print(code)
			time.sleep(5)
			passFlag = False
			caiWu = catchStockCaiWu(code)
			if(not caiWu):
				f.write(code+',')
				continue
			if(caiWu.retainedProfits < 0):	#净利润
				passFlag = True
			if(caiWu.IncomeYOYRate < 0):	#营收同比率
				passFlag = True
			if(caiWu.ProfitsYOYRate < 0):	#净利润同比
				passFlag = True
			if(caiWu.mainBusinessIncome < 10000):	#总营收
				passFlag = True
			if(caiWu.totalCapital < 5000000000):	#总市值
				passFlag = True
			
			codeFalg = '0'
			if(code[0] == '0'):
				codeFalg = '1'
			time.sleep(3)
			rb = requests.get(urlHistory.format(codeFalg, code, dayStart))
			rb.encoding = 'gb2312'
			list = rb.text.split('\r\n')
			list.pop(0)
			list.pop()
			if(len(list) < 3):
				passFlag = True
			elif( float(list[0].split(',')[4]) == 0 ):
				passFlag = True
				
			if(passFlag):
				f.write(code+',')
				continue
			
			candleList = []
			kdjList = [stock.KDJEn(caiWu.name, 50), ]
			for line in reversed(list):
				data = line.split(',')
				if( float(data[3]) == 0 ):
					continue
				candleList.append( stock.CandleEn( data[2], float(data[6]), float(data[3]), data[0], '', high=float(data[4]), low=float(data[5]), volume=int(data[11]), pmoney=float(data[12]) ) )
				kdjList.append(utils.kdjCalculate(candleList, kdjList))
				#测试
				#if(code == '002860'):
					#utils.printObjVal(kdjList[-1])
			popList = []
			isCode = False
			for i in range(3):
				if(utils.buyKdjCondition(kdjList)):
					if(len(popList) > 0):
						if( popList[0].k - kdjList[-1].k > 0 and popList[0].d - kdjList[-1].d > 0 and popList[0].j - kdjList[-1].j > 0 ):
							print(kdjList[-1].name, code)
							isCode = True
					else:
						print(kdjList[-1].name, code)
						isCode = True
					break
				popList.append(kdjList.pop())
			if(not isCode):
				f.write(code+',')
			#测试
			#if(code == '002863'):
				#pltDrawKDJ(kdjList)
				#pltDrawCandle2(candleList)
	
if __name__=='__main__':
	"""
	en = catchStockCaiWu('600756')
	utils.printObjVal(en)
	if(en.ProfitsYOYRate < 0):
		print('====')
	"""
	main_func()
	
	

