# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 17:07:00 2018

@author: BelskyJ
"""

import openpyxl
import pandas as pd
import numpy as np
import os
import glob
import argparse
from collections import OrderedDict

import classmatrix

def GetClassFriendshipMatrix(_friendship_df):

	# Initialize the class_friendship_matrix
	classFriendship_mat = np.empty(_friendship_df.shape, dtype = object)

	# Iterate through each row
	for i in range(0, classFriendship_mat.shape[0]):

		for j in range(classFriendship_mat.shape[1]):

			# Get the given and received status
			isGiven = True if _friendship_df.iloc[i, j] == 1 else False
			isReceived = True if _friendship_df.iloc[i, j] == 1 else False

			if isGiven and isReceived:
				classFriendship_mat[i, j] = "reciprocated"
			elif isGiven:
				classFriendship_mat[i, j] = "given"
			elif isReceived:
				classFriendship_mat[i, j] = "received"
			else:
				classFriendship_mat[i, j] = "none"

	# Return the friendship matrix
	return classFriendship_mat

parser = argparse.ArgumentParser()
parser.add_argument("friendship_nom_file", help = "Friendship Nominations File (.xlsx)")
parser.add_argument("peer_provisions_dir", help = "Directory containing peer provisions")
parser.add_argument("-o", "--output", action = "store", default = "compare_excel_dirs.txt", type = str)
args = parser.parse_args()

# Load in the friendship matrix
wb = openpyxl.load_workbook(args.friendship_nom_file)
class_sn = wb.sheetnames
class_sn.sort()

# Set up the friendship_matrix dict
classFriendship_dict = OrderedDict()

for c in class_sn:

	# Import the nominations matrix
	friendship_df, gender_s = classmatrix.GetDataMatrix(wb[c])

	# Get the friendship matrix
	classFriendship_dict[c] = GetClassFriendshipMatrix(friendship_df)

# Load in each of the provision matrices
peerProv_xlsx_files = glob.glob(args.peer_provisions_dir + "/*xlsx")
peerProv_xlsx_files.sort()

# Iterate through each peer provision
for pp_xls in peerProv_xlsx_files:

	pp_wb = openpyxl.load_workbook(pp_xls)

	# Iterate through each class_sn
	for c in class_sn:

		try:
			data_df, gender_s = classmatrix.GetDataMatrix(pp_wb[c])
		except:
			print("%s is not in %s, skipping..." % (c, pp_xls))
			continue
'''

# Load in the peer provisions
for pp_xls in peerProv_xls_files:

	pp_wb = openpyxl.load_workbook(pp_xls)

	for sheet_name in pp_wb.sheetnames:

		if "Class" not in sheet_name:
			continue

		print("%s\t%s" % (os.path.basename(pp_xls), sheet_name))



		break

	break

'''