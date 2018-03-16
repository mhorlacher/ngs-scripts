from __future__ import print_function
import numpy as np
import sys

in_fname = sys.argv[1]
mafThreshold = float(sys.argv[2])
out_fname = sys.argv[3]

#Open out-file
out_f = open(out_fname, 'w')

count_processed = 0
count_noInfo = 0
count_filtered = 0

#Scanning .vcf-file
with open(in_fname, 'r') as in_f:
	for line in in_f:
		#Writing headder
		if (line.strip())[0] == '#': 
			print(line.strip(), file=out_f)
			continue

		count_processed += 1

		#Extract DBSNP-Data
		line_cols = (line.strip()).split('\t')
		INFO = (line_cols[7]).split(';')

		DBSNP_CAF = ""
		DBSNP_OVL_CAF = ""

		for INFO_field in INFO:
			if INFO_field[:len("DBSNP_CAF")] == "DBSNP_CAF":
				DBSNP_CAF = INFO_field

			if INFO_field[:len("DBSNP_OVL_CAF")] == "DBSNP_OVL_CAF":
				DBSNP_OVL_CAF = INFO_field


		#DBSNP-Info missing - skip
		if not DBSNP_CAF:
			print(line.strip(), file=out_f)
			count_noInfo += 1
			continue

		#Get Allele Frequencies
		alleleFreqs = (DBSNP_CAF.split('=')[1]).split(',')
		alleleFreqs = [float(i) for i in alleleFreqs]
		alleleFreqs = sorted(alleleFreqs, reverse=True)

		#Get MAF (second largest freq.)
		MAF = alleleFreqs[1]

		#Filter Variant
		if MAF >= mafThreshold:
			count_filtered += 1
			
			if line_cols[6] == "PASS" || line_cols[6] == "."
				line_cols[6] = "fMAF"+str(mafThreshold)
			new_line = ""
			
			for col in line_cols:
				new_line += col+"\t"			
			print(new_line.strip(), file=out_f)

		else:
			print(line.strip(), file=out_f)

out_f.close()


#Open out-file
out_metrics_f = open(out_fname[:-3]+"metrics.txt", 'w')
print("# processed variants: "+str(count_processed), file=out_metrics_f)
print("# of variants without DBSNP-Info: "+str(count_noInfo), file=out_metrics_f)
print("# of variants filtered: "+str(count_filtered), file=out_metrics_f)
out_metrics_f.close()
























