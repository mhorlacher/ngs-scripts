import numpy as np
import sys

#.vcf-file
fname = sys.argv[1]

linesCount = 0
varCategories = {}

annotatedFlag = 1
errorLog = []

#Scanning .vcf-file
with open(fname, 'r') as f:
	for line in f:
		#skip headder
		if line[0] == '#': 
			continue

		#Count total number of Variants
		linesCount += 1

		# Get INFO field
		vcfLine = (line.strip()).split('\t')

		INFO = vcfLine[7]
		INFO = (INFO.strip()).split(';')

		#Scanning INFO for ANN-field
		ANN = []

		ANN_pos = -1
		f_count = 0
		for key in INFO:
			if key[:3] == "ANN":
				ANN_pos = f_count
			f_count += 1
		
		if ANN_pos != -1:
			ANN = (INFO[ANN_pos].strip()).split('|')
		else:
			errorLog.append(str(varCount)+": 'ANN'-field not found")


		#Count Variants of different Categories
		if ANN_pos != -1:
			varType = ANN[1]

			if varType in varCategories: 
				varCategories[varType] += 1
			else:
				varCategories[varType] = 1
		else:
			annotatedFlag = 0

print ""
print "Total lines: "+str(linesCount)
print""
if annotatedFlag:
	varCount = 0
	for key in sorted(varCategories, key=varCategories.get, reverse=True):
		if key != "":
			print str(key)+": "+str(varCategories[key])
			varCount += varCategories[key]
	print ""
	print "Total Variants: "+str(varCount)
else:
	print "VCF-File not annotated"
print ""






