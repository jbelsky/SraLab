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
import re
from collections import OrderedDict

import classmatrix

# Set up the new class
class OParkStudent:

	def __init__(self, _studentID, _gender):

		self.studentID = _studentID
		self.gender = _gender

	def set_friendship_array(self, _friendship_npArray):

		self.friendship_npArray = _friendship_npArray


	def init_peer_provision_df(self, _friendship_df, numProvisions):

		self.peerProvision_df = pd.DataFrame(index = _friendship_df.index, columns = range(1, numProvisions + 1))


def GetPeerProvisions(_dir):

	# Initialize the peerProvision matrix
	peerProv_dict = {}

	# Obtain the number of peer provision matrices
	peerProv_xlsx_files = glob.glob(_dir + "/*xlsx")
	peerProv_xlsx_files.sort()

	# Get the peer provision item -> file dict
	p = re.compile("Peer provisions item (\d{1,2})_.*\.xlsx")

	for f in peerProv_xlsx_files:

		item = p.match(os.path.basename(f)).group(1)
		peerProvItemFile_dict[item] = {}

		pp_wb = openpyxl.load_workbook(f)

		for OPclass in pp_wb.sheetnames:

			if "Class" not in OPclass:
				continue

			data_df, gender_s = classmatrix.GetDataMatrix(pp_wb[OPclass])

			# Enter into dict
			peerProvItemFile_dict[item][OPclass] = data_df

		pp_wb.close()

		return peerProvItemFile_dict


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
OPclass_dict = OrderedDict()

for c in class_sn:

	# Import the nominations matrix
	friendship_df, gender_s = classmatrix.GetDataMatrix(wb[c])

	# Get the friendship matrix
	friendship_mat = GetClassFriendshipMatrix(friendship_df)

	# Initialize the students
	student_dict = OrderedDict()
	for i in range(0, friendship_df.shape[0]):

		stuOP = OParkStudent(friendship_df.index[i], gender_s.iloc[i])
		stuOP.set_friendship_array(friendship_mat[i,:])
		stuOP.init_peer_provision_df(friendship_df, len(peerProv_xlsx_files))

		# Enter into the student_dict
		student_dict[stuOP.studentID] = stuOP

	break

wb.close()

'''
# Initialize the provisions_matrix dict
provisionsByClass_dict = OrderedDict()



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