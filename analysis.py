# -*- coding: utf-8 -*-
import utils, handledata
import configparser, time, pdb, threading, os, csv

if __name__=='__main__':
	#conf = configparser.ConfigParser()
	#conf.read('config.conf')
	#originalDir = conf.get('stock', 'originalDir')
	originalDir = handledata.originalDir
	pointNames = handledata.pointNames
	fileList = utils.getFilesByDir(originalDir + os.sep + 'stock', suffix = '.cvs')
	handledata.init_origi()
	for filePath in fileList:
		with open(filePath) as f:
			reader = csv.reader(f)
			for data in reader:
				handledata.dealOrigeData(data)
				if(data[0] in pointNames):
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

