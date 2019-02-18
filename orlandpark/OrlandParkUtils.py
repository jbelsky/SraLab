# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 17:07:00 2018

@author: BelskyJ
"""

import openpyxl
import pandas as pd
import os
import glob
import argparse
import re
from collections import OrderedDict

#from orlandpark import classmatrix
#from orlandpark import OParkClass
#from orlandpark import OParkStudent

def GetPeerProvisions(_dir):

	# Initialize the peerProvision matrix
	classPeerProvisionByItem_dict = {}

	# Obtain the number of peer provision matrices
	peerProv_xlsx_files = glob.glob(_dir + "/*xlsx")
	peerProv_xlsx_files.sort()

	# Get the peer provision item -> file dict
	p = re.compile("Peer provisions item (\d{1,2})_.*\.xlsx")

	for f in peerProv_xlsx_files:

		print(f)

		item = int(p.match(os.path.basename(f)).group(1))
		classPeerProvisionByItem_dict[item] = {}

		pp_wb = openpyxl.load_workbook(f)

		for OPclass in pp_wb.sheetnames:

			if "Class" not in OPclass:
				continue

			data_df, gender_s = classmatrix.GetDataMatrix(pp_wb[OPclass])

			# Enter into dict
			classPeerProvisionByItem_dict[item][OPclass] = data_df

		pp_wb.close()

	return classPeerProvisionByItem_dict


def GetClassFriendshipForEachStudent(_friendship_df, ARG_GENDER_SRS):

	# Initialize the class_friendship dict
	classFriendship_dict = OrderedDict()

	# Iterate through each row
	for i in _friendship_df.index:

		# Initialize the student series
		studentFriendship_df = pd.DataFrame(index = _friendship_df.columns, columns = ["Type", "Gender"], dtype = str)
		studentFriendship_df["Gender"] = ARG_GENDER_SRS

		# Drop the current student from the studentFriendship_srs
		studentFriendship_df.drop(index = i, inplace = True)

		for j in studentFriendship_df.index:

			given = _friendship_df.loc[i, j]
			received = _friendship_df.loc[j, i]

			if (given == 9) | (received == 9):
				studentFriendship_df.loc[j, "Type"] = "NA"
				continue

			# Get the given and received status
			isGiven = True if given == 1 else False
			isReceived = True if received == 1 else False

			if isGiven and isReceived:
				fsType = "reciprocated"
			elif isGiven:
				fsType = "given"
			elif isReceived:
				fsType = "received"
			else:
				fsType = "none"

			studentFriendship_df.loc[j, "Type"] = fsType

		# Add to the dict
		classFriendship_dict[i] = studentFriendship_df

	# Return the friendship matrix
	return classFriendship_dict
