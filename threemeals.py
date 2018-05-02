# -*- coding: utf-8 -*-
import configparser, time, threading
import stock, handledata
#from multiprocessing import Pool

def stockData(stockCode):
	print(stockCode, 'strating...')
	handledata.handleStock(stockCode)
	
def bigPan(code):
	print(code, 'strating big pan...')
	handledata.bigPanData(code)

if __name__=='__main__': 
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	threadList = []
	#stock
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		t = threading.Thread(target=stockData, args=(stockCode,))
		t.start()
		threadList.append(t)
	#big pan data
	for code in conf.get('stock', 'bigPanCodes').split(','):
		t = threading.Thread(target=bigPan, args=(code,))
		t.start()
		threadList.append(t)
		
	for t in threadList:
		t.join()

"""
#多进程方法
if __name__=='__main__': 
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	codeList = conf.get('stock', 'stockCodes').split(',')
	#i = 0
	print('Parent process %s.' % os.getpid())
	p = Pool(len(codeList))
	for stockCode in codeList:
		p.apply_async(handleData, args=(stockCode,))
		#i += 1
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')
"""