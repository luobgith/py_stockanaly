# -*- coding: utf-8 -*-
import utils, handledata
import configparser, time, pdb, threading

if __name__=='__main__':
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	originalDir = conf.get('stock', 'originalDir')
	#threadList = []
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		fileList = utils.getFilesByDir(originalDir + stockCode)
		#每一个都分析
		"""
		for filePath in fileList:
			print(filePath)
			t = threading.Thread(target=handledata.filesStock, args=(filePath, stockCode, ))
			t.start()
			t.join()
		"""
		
		#只分析最新的，与实际一样
		if(len(fileList) > 0):
			t = threading.Thread(target=handledata.filesStock, args=(fileList[-1], stockCode, ))
			t.start()
			#threadList.append(t)
			
"""	
	for t in threadList:
		t.join()
"""

