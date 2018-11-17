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

import classmatrix

parser = argparse.ArgumentParser()
parser.add_argument("friendship_nom_file", help = "Friendship Nominations File (.xlsx)")
parser.add_argument("peer_provisions_dir", help = "Directory containing peer provisions")
parser.add_argument("-o", "--output", action = "store", default = "compare_excel_dirs.txt", type = str)
args = parser.parse_args()

# Load in the friendship matrix
wb = openpyxl.load_workbook(args.friendship_nom_file)
class_sn = wb.sheetnames
class_sn.sort()

for c in class_sn:

	friendship_df, gender_s = classmatrix.GetDataMatrix(wb[c])

	given = np.array(friendship_df.iloc[:,0], dtype = np.int)
	received = np.array(friendship_df.iloc[0], dtype = np.int)
	friendship_status = np.empty(given.size, dtype = object)

	for i in range(0, friendship_status.size):

		# Get the given and received status
		isGiven = True if given[i] == 1 else False
		isReceived = True if received[i] == 1 else False

		if isGiven and isReceived:
			friendship_status[i] = "reciprocated"
		elif isGiven:
			friendship_status[i] = "given"
		elif isReceived:
			friendship_status[i] = "received"
		else:
			friendship_status[i] = "none"

	break

# Get the friendship status

'''

# Load in the peer provisions
peerProv_xls_files = glob.glob("c:/usr/opt/cygwin64/home/belskyj/JAB_GitHub/SraLab/data/Orland_Park/Peer_Provisions/*.xlsx")
peerProv_xls_files.sort()
for pp_xls in peerProv_xls_files:

	pp_wb = openpyxl.load_workbook(pp_xls)

	for sheet_name in pp_wb.sheetnames:

		if "Class" not in sheet_name:
			continue

		print("%s\t%s" % (os.path.basename(pp_xls), sheet_name))

		data_df, gender_s = classmatrix.GetDataMatrix(wb[sheet_name])

		break

	break

'''