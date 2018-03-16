from __future__ import print_function
import numpy as np
import sys

#.vcf-file
fname_in = sys.argv[1]
fname_out = sys.argv[2]

#Open out-file
out_f = open(fname_out, 'w')

count_processed = 0
count_removed = 0

#Scanning .vcf-file
with open(fname_in, 'r') as in_f:
	for line in in_f:
		#Writing headder
		if (line.strip())[0] == '#': 
			print(line.strip(), file=out_f)
			continue

		count_processed += 1

		line_cols = (line.strip()).split('\t')

		#Get ALT-field
		ALT = line_cols[4]
		ALT = ALT.split(',')

		#Check if multiple alternative Alleles exist
		if len(ALT) == 1:
			print(line.strip(), file=out_f)
			continue

		#Check if duplicate ALT-Allele exists
		dupPos = []
		dupPosALT = []
		dupCheck = False
		for i in range(0,len(ALT)):
			for j in range(i+1, len(ALT)):
				if ALT[i] == ALT[j]:
					dupPos.append(j)
					dupPosALT.append(i)
					dupCheck = True

		if dupCheck:
			count_removed += 1

			## Generating new ALT-Field
			ALT_NEW_A = [ALT[i] for i in range(0,len(ALT)) if i not in dupPos]
			#print(str(count_removed)+" ALT_NEW: "+str(ALT_NEW_A))

			ALT_NEW_S = ""
			for allele in ALT_NEW_A:
				ALT_NEW_S += allele+","
			ALT_NEW_S = ALT_NEW_S[:-1]

			## Generating new Genotypes
			for i in range(9,len(line_cols)):
				for j in range(0,len(dupPos)):
					if ((line_cols[i])[0] == str(dupPos[j]+1)):
						#print(str(count_removed)+" Before: "+line_cols[i])
						line_cols[i] = (str(dupPosALT[j]+1)+(line_cols[i])[1:])
						#print(str(count_removed)+" After : "+line_cols[i])

					if ((line_cols[i])[2] == str(dupPos[j]+1)):
						#print(str(count_removed)+" Before: "+line_cols[i])
						line_cols[i] = (line_cols[i])[0:2]+str(dupPosALT[j]+1)+(line_cols[i])[3:]
						#print(str(count_removed)+" After : "+line_cols[i])

			## Generating new Line
			LINE_NEW_A = line_cols
			LINE_NEW_A[4] = ALT_NEW_S

			LINE_NEW_S = ""
			for col in LINE_NEW_A:
				LINE_NEW_S += col+'\t'
			LINE_NEW_S = LINE_NEW_S[:-1]

			print(LINE_NEW_S, file=out_f)


		else:
			#Filter passed - print line
			print(line.strip(), file=out_f)

out_f.close()

print("Variants processed: "+str(count_processed))
print("Duplicate ALT-Alleles removed: "+str(count_removed))






