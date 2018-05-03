# -*- coding: utf-8 -*-
import configparser, time, threading
import stock, handledata
#from multiprocessing import Pool

if __name__=='__main__': 
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	threadList = []
	#stock
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		t = threading.Thread(target=handledata.onlineStock, args=(stockCode,))
		t.start()
		print(stockCode, 'thread is starting...')
		threadList.append(t)
	#big pan data
	for code in conf.get('stock', 'bigPanCodes').split(','):
		t = threading.Thread(target=handledata.onlineBigpan, args=(code,))
		print(code, 'thread is starting...')
		t.start()
		threadList.append(t)
"""		
	for t in threadList:
		t.join()
"""
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