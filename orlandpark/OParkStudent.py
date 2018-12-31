import pandas as pd
import numpy as np
import itertools
from collections import OrderedDict

# Set up the new OParkStudent class
class OParkStudent:

	def __init__(self, _studentID, _gender):

		self.studentID = _studentID
		self.gender = _gender

		self.oParkClass = None

		# Initialize other variables
		self.metricByItem_df = pd.DataFrame()
		self.receivedPeerProv_df = pd.DataFrame()

	def get_item_friendship_metrics(self, _itemNum):

		return self.metricByItem_df.loc[_itemNum]

	def set_oParkClass(self, _oParkClass):
		self.oParkClass = _oParkClass

	def set_received_peerprov_df(self):

		self.receivedPeerProv_df = pd.DataFrame(index = self.oParkClass.get_studentIDs(),
											    columns = list(self.oParkClass.peerProvisions_dict.keys()),
											    dtype = int
											   )

		# Fill in the data frame from the OParkClass
		for item, prov_df in self.oParkClass.peerProvisions_dict.items():
			self.receivedPeerProv_df.loc[:,item] = prov_df.loc[:,self.studentID]

		# Remove the current student from the matrix
		self.receivedPeerProv_df.drop(index = self.studentID, inplace = True)

	def set_received_friendships(self):

		self.receivedFriendships = self.oParkClass.get_friendship_srs(self.studentID)

		# Remove the current student from the vector
		self.receivedFriendships.drop(index = self.studentID, inplace = True)

	def get_number_of_item_fr_provs(self, _friendshipType, _provType, _itemNum):

		fr = self.receivedFriendships == _friendshipType
		prov =  self.receivedPeerProv_df[_itemNum] == _provType

		return np.where(fr & prov)[0].shape[0]

	def get_friendship_prov_gender(self, _friendshipType, _provType, _itemNum, _genderType):

		fr = self.receivedFriendships == _friendshipType
		prov = self.receivedPeerProv_df[_itemNum] == _provType

		# Get the class genders and drop the current studentID
		classGenders = self.oParkClass.get_student_genders()
		classGenders.drop(index = self.studentID, inplace = True)

		# Get the selection
		if _genderType == "sameGender":
			genderID = self.gender
		elif _genderType == "crossGender":
			genderID = 1 - self.gender

		gend = classGenders == genderID

		return np.where(fr & prov & gend)[0].shape[0]

	def set_provision_stats(self):

		# Set the possible friendship and provision types
		friendshipTypes = ["reciprocated", "given", "received", "none", "NA"]
		provisionTypes = [0, 1, 9]
		genderSubsets = ["sameGender", "crossGender"]

		# Get the tuple groupings
		frProvTypes = list(itertools.product(friendshipTypes, provisionTypes, genderSubsets))
		df_columns = [",".join([str(y) for y in x]) for x in frProvTypes]
		df_columns += ["ClassSize_FriendshipProvisionDefined", "NumberPeerProvisionsReceived"]

		# Initialize the storage dataframe
		metricByItem_df = pd.DataFrame(index = self.receivedPeerProv_df.columns,
                                       columns = df_columns
                                      )

		return metricByItem_df


	def set_provision_received_by_friendship_status(self):

		# Set the possible friendship and provision types
		friendshipTypes = ["reciprocated", "given", "received", "none", "NA"]
		provisionTypes = [0, 1, 9]

		# Get the tuple groupings
		frProvTypes = list(itertools.product(friendshipTypes, provisionTypes))
		df_columns = [fr + "," + str(prov) for fr, prov in frProvTypes]
		df_columns += ["ClassSize_FriendshipProvisionDefined", "NumberPeerProvisionsReceived"]

		frProvPropTypes = list(itertools.product(friendshipTypes[0:4], ["ClassSizeProp", "ReceivedProvisionProp"]))
		df_columns += ["_".join(tup) for tup in frProvPropTypes]

		# Initialize the storage dataframe
		metricByItem_df = pd.DataFrame(index = self.receivedPeerProv_df.columns,
											 columns = df_columns
											)

		# Iterate through each item
		for itemNum in metricByItem_df.index:

			for fr,prov in frProvTypes:

				metricByItem_df.loc[itemNum, fr + "," + str(prov)] = self.get_number_of_item_fr_provs(fr, prov, itemNum)

			# Get additional stats for the classes
			# Get sum of provisions types where friendship/provision is defined
			subsetCols = ~metricByItem_df.columns.str.contains("NA|,9", case = True, regex = True)
			metricByItem_df.loc[itemNum, "ClassSize_FriendshipProvisionDefined"] = metricByItem_df.loc[itemNum, subsetCols].sum()

			# Get the number of received provisions
			subsetCols = metricByItem_df.columns.str.contains("^(?!NA).*,1", case = True, regex = True)
			metricByItem_df.loc[itemNum, "NumberPeerProvisionsReceived"] = metricByItem_df.loc[itemNum, subsetCols].sum()

			# Get the proportions
			for fr,size in frProvPropTypes:
				frProvRec = metricByItem_df.loc[itemNum, fr + ",1"]
				if size == "ClassSizeProp":
					denom = metricByItem_df.loc[itemNum, "ClassSize_FriendshipProvisionDefined"]
				elif size == "ReceivedProvisionProp":
					denom = metricByItem_df.loc[itemNum, "NumberPeerProvisionsReceived"]

				# Get the ratio (if denominator of ratio is 0, define as 0)
				try:
					metricByItem_df.loc[itemNum, fr + "_" + size] = frProvRec / denom
				except:
					metricByItem_df.loc[itemNum, fr + "_" + size] = 0

		self.metricByItem_df = metricByItem_df

