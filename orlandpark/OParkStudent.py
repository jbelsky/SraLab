import pandas as pd
import numpy as np
import itertools
from collections import OrderedDict

from . import OParkFriend

# Set up the new OParkStudent class
class OParkStudent:

	FRIENDSHIP_TYPES = ["reciprocated", "given", "received", "none", "nominated", "not nominated", "NA"]
	NOMINATED_FRIENDSHIP_TYPES = ["reciprocated", "given", "nominated"]
	GENDER_SUBSET = ["all", "same", "cross"]

	def __init__(self, ARG_STUDENT_ID, ARG_GENDER, ARG_OPARKCLASS = None):

		self.studentID = ARG_STUDENT_ID
		self.gender = ARG_GENDER
		self.friends = OrderedDict()
		self.missing = False

		# Initialize other variables
		self.metricByItem_df = pd.DataFrame()
		self.receivedPeerProv_df = pd.DataFrame()

	def init_class_friendships(self, ARG_OPARKCLASS_STUDENTS, ARG_FRIENDSHIP_DF):

		# Check if student is missing
		if all(ARG_FRIENDSHIP_DF.loc[self.studentID] == 9):
			self.missing = True

		# Iterate through the other students in the class
		for i, ops in ARG_OPARKCLASS_STUDENTS.items():

			if i == self.get_id():
				continue

			opf = OParkFriend.OParkFriend(self, ops)
			opf.set_friendship_type(ARG_FRIENDSHIP_DF)

			self.friends[i] = opf

	def get_id(self):
		return self.studentID

	def get_gender(self):
		return self.gender

	def get_summary_by_friendship(self, ARG_FRIENDSHIP_TYPE, ARG_GENDER_TYPE = "all"):

		# Initialize the ct
		ct = 0
		
		for i, opf in self.friends.items():

			if opf.get_friendship_type() == ARG_FRIENDSHIP_TYPE:

				if ARG_GENDER_TYPE == "all" or opf.get_gender_relationship() == ARG_GENDER_TYPE:
					ct += 1

		return ct

	def get_number_of_friendship_types(self):

		frGenPairs = list(itertools.product(OParkStudent.FRIENDSHIP_TYPES[0:4], OParkStudent.GENDER_SUBSET))
		cts = []

		for f, g in frGenPairs:

			cts.append(self.get_summary_by_friendship(f, g))

		return pd.Series(cts, index = ["%s_%s" % x for x in frGenPairs])

	def get_number_of_nominations(self):

		cts = []
		for g in OParkStudent.GENDER_SUBSET:

			num = 0

			for f in OParkStudent.NOMINATED_FRIENDSHIP_TYPES:

				num += self.get_summary_by_friendship(f, g)

			cts.append(num)

		return pd.Series(cts, index = ["total_nominated_%s" % i for i in OParkStudent.GENDER_SUBSET])










	def get_item_friendship_metrics(self, _itemNum):

		return self.metricByItem_df.loc[_itemNum]


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

		receivedFriendships = self.oParkClass.get_friendship_srs(self.studentID)

		# Remove the current student from the vector
		self.receivedFriendships = receivedFriendships.drop(index = self.studentID)

	def get_number_of_item_fr_provs(self, _friendshipType, _provType, _itemNum):

		fr = self.receivedFriendships == _friendshipType
		prov =  self.receivedPeerProv_df[_itemNum] == _provType

		return np.where(fr & prov)[0].shape[0]

	def get_friendship_prov_gender(self, _friendshipType, _provType, _genderType, _itemNum):

		fr = self.receivedFriendships == _friendshipType
		prov = self.receivedPeerProv_df[_itemNum] == _provType

		# Get the class genders and drop the current studentID
		classGenders = self.oParkClass.get_friendship_genders(self.studentID)

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
		frProvGend = list(itertools.product(friendshipTypes, provisionTypes, genderSubsets))
		df_columns = [",".join([str(y) for y in x]) for x in frProvGend]
		# df_columns += ["ClassSize_FriendshipProvisionDefined", "NumberPeerProvisionsReceived"]

		# Initialize the storage dataframe
		metricByItem_df = pd.DataFrame(index = self.receivedPeerProv_df.columns,
                                       columns = df_columns
                                      )

		# Iterate through each item
		for itemNum in metricByItem_df.index:

			for fpg in frProvGend:

				# Get the friendship, provision, and gender types
				fr = fpg[0]
				pr = fpg[1]
				ge = fpg[2]

				frPrGeItemCt = self.get_friendship_prov_gender(fr, pr, ge, itemNum)
				metricByItem_df.loc[itemNum, ",".join([str(y) for y in fpg])] = frPrGeItemCt

		self.metricByItem_df = metricByItem_df


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

