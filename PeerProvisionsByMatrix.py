# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:16:15 2018

Updated: 2018-09-30

@author: jab112
"""

import openpyxl
import pandas as pd
import numpy as np
import re
import argparse
import itertools
from collections import OrderedDict
import glob
import os
import sys

import classmatrix

# Define class variables
GENDER_COMPS = ["AllGender", "ByGender", "CrossGender"]
ANALYSIS_TYPES = ["Given", "Received"]

def GetDfCols():

	# Create the output for each type [AllGender, ByGender, CrossGender]
	analysisCols = ["_".join(x) + "_mean" for x in itertools.product(GENDER_COMPS, ANALYSIS_TYPES)]

	# Prepend with "Gender"
	outputCols = ["Gender"] + analysisCols

	return outputCols


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


# Store the output_df
allItems_d = OrderedDict()

# Get all the xls files by directory
xlsFiles = glob.glob(args.input_xls_dir + "/*.xlsx")

# Initialize the item2File mapping
item2FileDict = {}

# Extract the item # from the filename
p = re.compile(r".*[iI]tem[-_ ](\d{1,2})[-_].*")

for x in xlsFiles:

	# Attempt to extract the item number
	m = p.match(os.path.basename(x))
	if m:
		key = "Item" + m.group(1)

	# Otherwise just default to basename
	else:
		print("ERROR: could not extract item number from '%s'" % os.path.basename(x))
		sys.exit(1)

	# Enter mapping into dict
	item2FileDict[key] = x

# Sort the item2FileDict keys and iterate through each item
itemKeys = list(item2FileDict.keys())
itemKeys.sort()

for item in itemKeys:

	# Initialize the class item dataframe
	classOutByItem = []

	# Load the workbook
	xlsFile = item2FileDict[item]
	wb = openpyxl.load_workbook(xlsFile)

	for sheet_name in wb.sheetnames:

		if "Class" not in sheet_name:
			print("'%s' does not have 'Class' as substring, skipping..." % sheet_name)
			continue

		print("%s\t%s" % (xlsFile, sheet_name))

		# Get the worksheet
		ws = wb[sheet_name]

		# Extract the data matrix and gender series
		data_df, gender_s = classmatrix.GetDataMatrix(ws)

		# Get the columns
		dfCols = GetDfCols()

		# Initialize the output dataframe
		out_df = pd.DataFrame(np.zeros(shape = (data_df.shape[0], len(dfCols))), 
							  columns = dfCols,
							  index = data_df.index
							 )
		out_df["Gender"] = gender_s.values

		for gComp, aType in itertools.product(GENDER_COMPS, ANALYSIS_TYPES):

			# Get the average score for each student
			for stuID in data_df.index:
	
				# Get the student average score
				out_df.loc[stuID, gComp + "_" + aType + "_mean"] = GetStuAvgScore(data_df, gender_s, stuID, gComp, aType)

		# Append each class output to the dataframe
		classOutByItem.append(out_df)
	
	# Store the output
	allItems_d[item] = pd.concat(classOutByItem).sort_index()
	
# Create the output workbook
f_out = args.input_xls_dir + "/PeerProvisionsByItemAnalysis.run2.xlsx"
writer= pd.ExcelWriter(f_out)
for k in allItems_d.keys():
	allItems_d[k].to_excel(writer, sheet_name = "Item_" + str(k), float_format = "%.4f", freeze_panes = (1, 1))

writer.save()

print("Analysis written to %s\n" % f_out)
