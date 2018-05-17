# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.mpl_finance as mpf
from matplotlib.pylab import date2num
import requests, csv, re, time
import stock, utils

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
url = 'http://quotes.money.163.com/service/chddata.html?code={0}{1}&start={2}'

codes = getStackCode(requests.get(urlCode).text)
codeList = []
for item in codes:
    if(item[0]=='6' or item[0]=='0'):
        codeList.append(item)

dayStart = (datetime.now() - timedelta(days=150)).strftime('%Y%m%d')
for code in codeList[-200: ]:
	codeFalg = '0'
	if(code[0] == '0'):
		codeFalg = '1'
	time.sleep(0.2)
	#contents = requests.get(url.format(codeFalg, code, dayStart)).text
	rb = requests.get(url.format(codeFalg, code, dayStart))
	rb.encoding = 'gb2312'
	#contents = rb.text
	list = rb.text.split('\r\n')
	list.pop(0)
	list.pop()
	if(len(list) < 3):
		continue
	tmp = 0
	for i in range(10):
		tmp += float(list[i].split(',')[4])
	if(tmp == 0):
		continue
		
	candleList = []
	kdjList = [stock.KDJEn('', 50), ]
	for line in reversed(list):
		data = line.split(',')
		candleList.append( stock.CandleEn( data[2], float(data[6]), float(data[3]), data[0], '', high=float(data[4]), low=float(data[5]), volume=int(data[11]), pmoney=float(data[12]) ) )
		kdjList.append(utils.kdjCalculate(candleList, kdjList))
		#测试
		#if(code == '002860'):
			#utils.printObjVal(kdjList[-1])
	for i in range(3):
		if(utils.buyKdjCondition(kdjList)):
			print(kdjList[-1].name, code)
			break
		kdjList.pop()
	#测试
	#if(code == '002863'):
		#pltDrawKDJ(kdjList)
		#pltDrawCandle2(candleList)
