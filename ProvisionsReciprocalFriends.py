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
import itertools
from collections import OrderedDict

import classmatrix

# Set up the new OPClass

class OParkClass:

	def __init__(self, _classID, _students_list, _friendship_dict, _allClassPeerProvisionsByItem_dict):

		self.classID = _classID
		self.students_list = _students_list
		self.friendships_dict = _friendship_dict

		self.peerProvisions_dict = OrderedDict()
		self.peerProvisions_items = list(_allClassPeerProvisionsByItem_dict)
		self.peerProvisions_items.sort()

		for i in self.peerProvisions_items:
			if self.classID in _allClassPeerProvisionsByItem_dict[i]:
				self.peerProvisions_dict[i] = _allClassPeerProvisionsByItem_dict[i][self.classID]

	def get_studentIDs(self):

		return [s.studentID for s in self.students_list]

	def get_studentID_index(self, _studentID):

		studentID_list = self.get_studentIDs()
		try:
			return studentID_list.index(_studentID)
		except:
			print("StudentID %d is not in %s" % (_studentID, self.classID))

	def get_peer_provisions_items(self):

		return self.peerProvisions_items

	def get_peer_provisions_item_df(self, _peerProvItem):

		return self.peerProvisions_dict[_peerProvItem]

	def get_friendship_dict(self, _studentID):
		return self.friendships_dict[_studentID]

	def set_item_summary(self):

		# Initialize the OrderedDict
		item_odict = OrderedDict()

		# Set the columnNames
		columnNames = self.students_list[0].receivedPeerProvByFriendshipStatus_df.columns

		# Iterate through each item and get each OParkStudent statistics
		for item in self.get_peer_provisions_items():

			itemStat_df = pd.DataFrame(index = self.get_studentIDs(),
										   columns = columnNames
										   )

			# Update the data frame for each student
			for ops in self.students_list:
				itemStat_df.loc[ops.studentID] = ops.get_item_friendship_metrics(item)

			item_odict[item] = itemStat_df

		self.itemStat_odict = item_odict

# Set up the new class
class OParkStudent:

	def __init__(self, _studentID, _gender):

		self.studentID = _studentID
		self.gender = _gender

	def get_item_friendship_metrics(self, _itemNum):

		return self.receivedPeerProvByFriendshipStatus_df.loc[_itemNum]

	def set_received_peerprov_df(self, _OPclass):

		self.receivedPeerProv_df = pd.DataFrame(index = _OPclass.get_studentIDs(),
											    columns = list(_OPclass.peerProvisions_dict.keys()),
											    dtype = int
											   )

		# Fill in the data frame from the OParkClass
		for item, prov_df in _OPclass.peerProvisions_dict.items():
			self.receivedPeerProv_df.loc[:,item] = prov_df.loc[:,self.studentID]

		# Remove the current student from the matrix
		self.receivedPeerProv_df.drop(index = self.studentID, inplace = True)

	def set_received_friendships(self, _OPclass):

		self.receivedFriendships = _OPclass.get_friendship_dict(self.studentID)

		# Remove the current student from the vector
		self.receivedFriendships.drop(index = self.studentID, inplace = True)

	def set_provision_received_by_friendship_status(self):

		# Set the possible friendship types
		friendshipTypes = ["reciprocated", "given", "received", "none"]
		suffix = ["OnlyReceivedProv", "All"]

		# Set the column names
		columnNames = ["Number_ClassFriendshipsAvailable",
						  "Number_Reciprocated",
						  "Number_Given",
						  "Number_Received",
						  "Number_NoFriendships",
						  "Number_NA_Friendships"
						 ]
		columnNames += ["_".join(x) for x in itertools.product(friendshipTypes, suffix)]

		# Initialize the storage dataframe
		summaryByItem_df = pd.DataFrame(index = self.receivedPeerProv_df.columns,
											  columns = columnNames
											 )

		# Iterate through each item
		for itemNum in summaryByItem_df.index:

			# Find the total number receiving provisions
			totalRecProv = np.where(self.receivedPeerProv_df[itemNum] == 1)[0].shape[0]
			classSize = np.where(self.receivedPeerProv_df[itemNum].isin([0, 1]))[0].shape[0]

			denom = (totalRecProv, classSize)

			# Set the total numbers
			recipAndItem = get_number_of_item_friendship_provs




			summaryByItem_df.loc[itemNum, "Number_ClassFriendshipsAvailable"] = classSize
			summaryByItem_df.loc[itemNum, "Number_Reciprocated"] = np.where((self.receivedFriendships == "reciprocated") & (self.receivedPeerProv_df[itemNum].isin([0, 1]))[0].shape[0]
			summaryByItem_df.loc[itemNum, "Number_Given"] = np.where(self.receivedFriendships == "given")[0].shape[0]
			summaryByItem_df.loc[itemNum, "Number_Received"] = np.where(self.receivedFriendships == "received")[0].shape[0]
			summaryByItem_df.loc[itemNum, "Number_NoFriendships"] = np.where(self.receivedFriendships == "none")[0].shape[0]
			summaryByItem_df.loc[itemNum, "Number_NA_Friendships"] = np.where(self.receivedFriendships == "NA")[0].shape[0]

			for fr in friendshipTypes:

				frAndRec = (self.receivedFriendships == fr) & (self.receivedPeerProv_df[itemNum] == 1)
				fr_recProv = np.where(frAndRec)[0].shape[0]

				# Enter proportion into data frame
				for i in (0, 1):

					if denom[i] > 0:
						proportion = fr_recProv / denom[i]
					else:
						proportion = 9

					summaryByItem_df.loc[itemNum, "_".join([fr, suffix[i]])] = proportion

		self.receivedPeerProvByFriendshipStatus_df = summaryByItem_df

	def get_number_friendship_type(self, _friendshipType):

		return np.where(self.receivedFriendships == _friendshipType)[0].shape[0]

	def get_number_of_item_friendship_provs(self, _friendshipType, _itemNum):

		frAndRec = (self.receivedFriendships == _friendshipType) & (self.receivedPeerProv_df[_itemNum] == 1)

		return np.where(frAndRec)[0].shape[0]


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


def GetClassFriendshipForEachStudent(_friendship_df):

	# Initialize the class_friendship dict
	classFriendship_dict = OrderedDict()

	# Iterate through each row
	for i in _friendship_df.index:

		# Initialize the student series
		studentFriendship_srs = pd.Series(index = _friendship_df.columns, dtype = str)

		for j in _friendship_df.columns:

			# Get the given and received status
			isGiven = True if _friendship_df.loc[i, j] == 1 else False
			isReceived = True if _friendship_df.loc[j, i] == 1 else False

			if isGiven and isReceived:
				studentFriendship_srs.loc[j] = "reciprocated"
			elif isGiven:
				studentFriendship_srs.loc[j] = "given"
			elif isReceived:
				studentFriendship_srs.loc[j] = "received"

			# NOTE: what to do about 9s for friendships?
			elif (_friendship_df.loc[i,j] == 9) | (_friendship_df.loc[j,i] == 9):
				studentFriendship_srs.loc[j] = "NA"
			else:
				studentFriendship_srs.loc[j] = "none"

		# Drop the current student from the series

		# Add to the dict
		classFriendship_dict[i] = studentFriendship_srs

	# Return the friendship matrix
	return classFriendship_dict

parser = argparse.ArgumentParser()
parser.add_argument("friendship_nom_file", help = "Friendship Nominations File (.xlsx)")
parser.add_argument("peer_provisions_dir", help = "Directory containing peer provisions")
parser.add_argument("-o", "--output", action = "store", default = "compare_excel_dirs.txt", type = str)
args = parser.parse_args()

# Get the peer provisions for each of the classes
classPeerProvisionsByItem_dict = GetPeerProvisions(args.peer_provisions_dir)

# Load in the friendship matrix
wb = openpyxl.load_workbook(args.friendship_nom_file)
class_sn = wb.sheetnames
class_sn.sort()

# Set up the friendship_matrix dict
OPclass_dict = OrderedDict()

for c in class_sn[0:5]:

	print("Working on %s..." % c)

	# Import the nominations matrix
	friendship_df, gender_srs = classmatrix.GetDataMatrix(wb[c])

	# Get the friendship dict
	friendship_dict = GetClassFriendshipForEachStudent(friendship_df)

	# Set the OParkStudent list
	OPstudent_list = [OParkStudent(i, gender_srs.loc[i]) for i in gender_srs.index]

	# Initialize an OPClass
	orlandParkClass = OParkClass(c, OPstudent_list, friendship_dict, classPeerProvisionsByItem_dict)

	# Iterate through each OParkStudent
	for ops in OPstudent_list:

		ops.set_received_peerprov_df(orlandParkClass)
		ops.set_received_friendships(orlandParkClass)
		ops.set_provision_received_by_friendship_status()

	# Get the class item summary
	orlandParkClass.set_item_summary()

	# Store the item statistics in the dict
	OPclass_dict[c] = orlandParkClass.itemStat_odict

wb.close()

# Create the output workbook
f_out = "FriendshipPeerProvisionsByItemAnalysis.xlsx"
writer= pd.ExcelWriter(f_out)

# Iterate through each item
items = list(classPeerProvisionsByItem_dict.keys())
items.sort()
for i in items[0:3]:

	# Get all the dataframes for the item in one list
	itemByClass = []
	for c, opc_d in OPclass_dict.items():
		itemByClass.append(opc_d[i])

	# Write the excel worksheet
	itemByClass_df = pd.concat(itemByClass, axis = 0, join = "inner")
	itemByClass_df.to_excel(writer, sheet_name = "Item_" + str(i), float_format = "%.4f", freeze_panes = (1, 1))

writer.save()