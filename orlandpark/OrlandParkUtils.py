import openpyxl
import pandas as pd
import os
import glob
import re
import sys
from collections import OrderedDict

from . import classmatrix

#from orlandpark import classmatrix
#from orlandpark import OParkClass
#from orlandpark import OParkStudent

def GetProvisions(ARG_PROV_DIR):

	# Initialize the peerProvision matrix
	provDict = {}

	# Obtain the number of peer provision matrices
	provXlsxFiles = glob.glob(ARG_PROV_DIR + "/*xlsx")
	provXlsxFiles.sort()

	# Get the peer provision item -> file dict
	p1 = re.compile("Peer provisions (item \d{1,2})_.*\.xlsx")
	p2 = re.compile("(Item \d{1,2})-.*\.xlsx")

	for provXlsxFile in provXlsxFiles:

		print(provXlsxFile)

		m1 = p1.match(os.path.basename(provXlsxFile))
		m2 = p2.match(os.path.basename(provXlsxFile))
		if m1:
			item = m1.group(1)
		elif m2:
			item = m2.group(1)
		else:
			print("Could not extract 'item' from provision Excel filename!")
			sys.exit(1)

		# Initialize the dict for the item
		provDict[item] = {}

		# Open the Excel file
		provXlsx = openpyxl.load_workbook(provXlsxFile)

		for className in provXlsx.sheetnames:

			if "Class" not in className:
				continue

			data_df, gender_s = classmatrix.GetDataMatrix(provXlsx[className])

			# Enter into dict
			provDict[item][className] = data_df

		provXlsx.close()

	return provDict


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
