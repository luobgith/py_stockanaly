# -*- coding: utf-8 -*-
import utils, handledata
import configparser, time, pdb

if __name__=='__main__':
	conf = configparser.ConfigParser()
	conf.read('config.conf')
	originalDir = conf.get('stock', 'originalDir')
	for stockCode in conf.get('stock', 'stockCodes').split(','):
		fileList = utils.getFilesByDir(originalDir + stockCode)
		for filePath in fileList:
			handledata.init()
			#pdb.set_trace()
			print(filePath)
			with open(filePath, 'r') as f:
				for line in f.readlines():
					handledata.analysisdata(line)
					#pass
		#print(fileList)


