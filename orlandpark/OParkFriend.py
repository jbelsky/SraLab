import pandas as pd
import numpy as np

class OParkFriend:

	def __init__(self, ARG_OPARKSTUDENT, ARG_OPARKSTUDENT_FRIEND):

		self.ops = ARG_OPARKSTUDENT
		self.opsFriend = ARG_OPARKSTUDENT_FRIEND

		# Initialize other variables
		self.friendType = None
		self.provisionsGiven = pd.Series(index = range(1, 13), dtype = int)

	def get_gender_relationship(self):

		if self.ops.get_gender() == self.opsFriend.get_gender():
			return "same"
		else:
			return "cross"

	def get_friendship_type(self):

		return self.friendType

	def set_provision(self, ARG_PROVISION, ARG_GIVEN):

		self.provisionsGiven.loc[ARG_PROVISION] = ARG_GIVEN

	def set_friendship_type(self, ARG_FRIENDSHIP_DF):

		stID1 = self.ops.get_id()
		stID2 = self.opsFriend.get_id()

		given = ARG_FRIENDSHIP_DF.loc[stID1, stID2]
		received = ARG_FRIENDSHIP_DF.loc[stID2, stID1]

		if given == 9 or received == 9:
			fsType = "NA"
		elif given == 1 and received == 1:
			fsType = "reciprocated"
		elif given == 1 and received == 0:
			fsType = "given"
		elif given == 0 and received == 1:
			fsType = "received"
		elif given == 0 and received == 0:
			fsType = "none"
		else:
			print("WARNING: Cannot determine friendshipType for '%d' and '%d'" % (stID1, stID2))
			fsType = "UNDETERMINED"

		self.friendType = fsType
