# -*- coding: utf-8 -*-
import utils, handledata
import configparser, time, pdb, threading

if __name__=='__main__':
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	originalDir = conf.get('stock', 'originalDir')
	threadList = []
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		fileList = utils.getFilesByDir(originalDir + stockCode)
		if(len(fileList) > 0):
			t = threading.Thread(target=handledata.filesStock, args=(fileList[-1], stockCode, ))
			t.start()
			threadList.append(t)
"""	
	for t in threadList:
		t.join()
"""
"""
		for filePath in fileList:
			handledata.init()
			#pdb.set_trace()
			print('')
			print(filePath)
			with open(filePath, 'r') as f:
				for line in f.readlines():
					handledata.analysisdata(line)
					#pass
		#print(fileList)
"""

