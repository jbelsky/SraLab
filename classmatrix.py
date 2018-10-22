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
import os
import glob
import re
import sys

def GetDataRange(_np_arr):

	# Find the beginning data type
	if any(_np_arr == "ID"):
		iStart = np.where(_np_arr == "ID")[0][0] + 1

	# Otherwise, find the first StudentID
	else:
		iStart = np.where(np.array([type(x) for x in _np_arr]) == int)[0][0]

	# Find the iEnd (last consecutive index that is an int)
	iEnd = iStart
	for i in range(iStart, len(_np_arr)):
		if type(_np_arr[i]) != int:
			iEnd = i - 1
			break
	if iEnd == iStart:
		iEnd = len(_np_arr)

	return (iStart, iEnd)


def GetDataMatrix(_ws):

	# Check matrix integrity
	columnA = np.array([c.value for c in _ws["A"]])
	row1 = np.array([c.value for c in _ws["1"]])

	# Check the StudentID
	iColumnA = GetDataRange(columnA)
	iRow1 = GetDataRange(row1)

	if iColumnA != iRow1:
		print("WARNING: ColumnA and Row1 have different start/end indices!")
		print(str(iColumnA[0]) + "\t" + str(iColumnA[1]))
		print(str(iRow1[0]) + "\t" + str(iRow1[1]))
		sys.exit(1)
	else:
		iStart = iColumnA[0]
		iEnd = iColumnA[1]
		stuID_arr = columnA[iStart:(iEnd + 1)]

	# Check the Gender indices
	columnB = np.array([c.value for c in _ws["B"]][iStart:(iEnd + 1)])
	row2 = np.array([c.value for c in _ws["2"]][iStart:(iEnd + 1)])

	if np.array_equal(columnB, row2):
		gender_arr = columnB
	else:
		print("WARNING: ColumnB and Row2 have different genders!")
		print(columnB)
		print(row2)
		sys.exit(1)

	# Make the data matrix
	rowList = []
	for row in _ws.iter_rows(min_row = iStart + 1, max_row = iEnd + 1, min_col = iStart + 1, max_col = iEnd + 1):
		rowList.append([c.value for c in row])

	# Convert to data frame
	data_df = pd.DataFrame(rowList, index = stuID_arr, columns = stuID_arr, dtype = int)
	gender_s = pd.Series(gender_arr, index = stuID_arr, dtype = int)

	# Return a data frame and gender dict
	return (data_df, gender_s)
