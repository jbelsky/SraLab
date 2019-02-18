import pandas as pd
import numpy as np

class OParkFriend:

	def __init__(self, ARG_ID, ARG_FRIEND_OF_ID):

		self.friendID = ARG_ID
		self.friendOfID = ARG_FRIEND_OF_ID

		# Initialize other variables
		self.friendType = None
		self.gender = None
		self.provisionsGiven = pd.Series(index = range(1, 13), dtype = int)

	def set_friendship_type(self, ARG_FRIEND_TYPE):
		self.friendType = ARG_FRIEND_TYPE

	def set_gender(self, ARG_GENDER):
		self.gender = ARG_GENDER

	def set_provision(self, ARG_PROVISION, ARG_GIVEN):
		self.provisionsGiven.loc[ARG_PROVISION] = ARG_GIVEN
