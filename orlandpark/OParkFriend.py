import pandas as pd
import numpy as np

class OParkFriend:

	def __init__(self, ARG_OPARKSTUDENT, ARG_OPARKSTUDENT_FRIEND):

		self.ops = ARG_OPARKSTUDENT
		self.opsFriend = ARG_OPARKSTUDENT_FRIEND

		# Initialize other variables
		self.friendType = None
		self.provisions = {}

	def get_gender_relationship(self):

		if self.ops.get_gender() == self.opsFriend.get_gender():
			return "same"
		else:
			return "cross"

	def get_friendship_type(self):

		return self.friendType

	def set_provision(self, PROVISION, TYPE, VALUE):

		# Initialize provision if doesn't exist
		if PROVISION not in self.provisions:
			self.provisions[PROVISION] = {}

		# Initialize given/received
		if TYPE not in self.provisions[PROVISION]:
			self.provisions[PROVISION] = {}

		# Add the value
		self.provisions[PROVISION][TYPE] = VALUE

	def set_friendship_type(self, ARG_FRIENDSHIP_DF):

		stID1 = self.ops.get_id()
		stID2 = self.opsFriend.get_id()

		given = ARG_FRIENDSHIP_DF.loc[stID1, stID2]
		received = ARG_FRIENDSHIP_DF.loc[stID2, stID1]

		if received == 9 and given == 1:
			fsType = "nominated"
		elif received == 9 and given == 0:
			fsType = "not nominated"
		elif given == 1 and received == 1:
			fsType = "reciprocated"
		elif given == 1 and received == 0:
			fsType = "given"
		elif given == 0 and received == 1:
			fsType = "received"
		elif given == 0 and received == 0:
			fsType = "none"
		elif given == 9 and received == 1:
			fsType = "received"
		elif given == 9:
			fsType = "NA"
		else:
			print("WARNING: Cannot determine friendshipType for '%d' and '%d'" % (stID1, stID2))
			fsType = "UNDETERMINED"

		self.friendType = fsType
