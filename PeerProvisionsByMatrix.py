# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:16:15 2018

Updated: 2018-09-30

@author: jab112
"""

import openpyxl
import pandas as pd
import numpy as np
import argparse
import itertools
from collections import OrderedDict
import glob
import os

import classmatrix

def GetStuAvgScore(_data_df, _gender_s, _id, _gender, _type):

	if _type == "Given":
		vals = _data_df.loc[_id]
	elif _type == "Received":
		vals = _data_df[_id]

	# Get scores != 9
	# See if there needs to be a gender filter
	idx = vals != 9
	if _gender == "ByGender":
		idx = idx & (_gender_s == _gender_s[_id])
	elif _gender == "CrossGender":
		idx = idx & (_gender_s != _gender_s[_id])

	# Subset on the score
	valsSubset = vals[idx] 
	
	# Get the percentage within the subset with "1"
	if len(valsSubset) > 0:
		return len(np.where(valsSubset == 1)[0]) / len(valsSubset)
	else:
		return 9


###################
# Begin script here
###################

parser = argparse.ArgumentParser()
parser.add_argument("input_xls_dir", help = "the directory containing all of the Excel files")
args = parser.parse_args()

# Create the output for each type [AllGender, ByGender, CrossGender]
genderComps = ["AllGender", "ByGender", "CrossGender"]
analysisTypes = ["Given", "Received"]
analysisCols = ["_".join(x) + "_mean" for x in itertools.product(genderComps, analysisTypes)]
	
# Store the output_df
allItems_d = OrderedDict()

for item in range(1,13):

	f_xls = glob.glob(args.input_xls_dir + "/Peer provisions item " + str(item) + "_*.xlsx")[0]
	wb = openpyxl.load_workbook(f_xls)

	classOutByItem = []

	for sheet_name in wb.get_sheet_names():
			
		if "Class" not in sheet_name:
			continue
		
		print("%s\t%s" % (os.path.basename(f_xls), sheet_name))
		
		
		ws = wb[sheet_name]
	
		data_df, gender_s = classmatrix.GetDataMatrix(ws)
		
		# Construct the output dataframe
		out_df = pd.DataFrame(np.zeros(shape = (data_df.shape[0], 7)), columns = ["Gender"] + analysisCols, index = data_df.index)
		out_df["Gender"] = gender_s.values
		
		for gComp, aType in itertools.product(genderComps, analysisTypes):
	
			# Get the average score for each student
			for stuID in data_df.index:
	
				# Get the student average score
				out_df.loc[stuID, gComp + "_" + aType + "_mean"] = GetStuAvgScore(data_df, gender_s, stuID, gComp, aType)
		
		classOutByItem.append(out_df)
	
	# Store the output
	allItems_d[item] = pd.concat(classOutByItem).sort_index()
	
# Create the output workbook
f_out = args.input_xls_dir + "/PeerProvisionsByItemAnalysis.xlsx"
writer= pd.ExcelWriter(f_out)
for k in allItems_d.keys():
	allItems_d[k].to_excel(writer, sheet_name = "Item_" + str(k))

writer.save()

print("Analysis written to %s\n" % f_out)