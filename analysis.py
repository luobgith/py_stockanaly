# -*- coding: utf-8 -*-
import utils, handledata, config
import configparser, time, pdb, threading, os, csv

if __name__=='__main__':
	#conf = configparser.ConfigParser()
	#conf.read('config.conf')
	#originalDir = conf.get('stock', 'originalDir')
	#originalDir = config.originalDir
	#pointNames = config.pointNames
	fileList = utils.getFilesByDir(config.originalDir + os.sep + 'stock', suffix = '.csv')
	handledata.init_origi()
	#fileList.pop()
	#fileList.pop()
	for filePath in fileList[-1: ]:
		with open(filePath) as f:
			reader = csv.reader(f)
			for data in reader:
				handledata.dealOrigeData(data)
				if(data[0] in config.pointNames):
					handledata.analysisOrgiData(data[0])
		handledata.init_origi()
	"""
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		fileList = utils.getFilesByDir(originalDir + stockCode)
		#每一个都分析
		
		for filePath in fileList:
			print(filePath)
			t = threading.Thread(target=handledata.filesStock, args=(filePath, stockCode, ))
			t.start()
			t.join()
		
		
		#只分析最新的，与实际一样
		if(len(fileList) > 0):
			t = threading.Thread(target=handledata.filesStock, args=(fileList[-1], stockCode, ))
			t.start()
			#threadList.append(t)
		"""	
"""	
	for t in threadList:
		t.join()
"""

