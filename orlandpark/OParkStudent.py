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

	def __init__(self, STUDENT_ID, GENDER):

		self.studentID = ARG_STUDENT_ID
		self.gender = ARG_GENDER
		self.friends = []

	def get_id(self):
		return self.studentID

	def get_gender(self):
		return self.gender

	def init_class_friendships(self, ARG_OPARKCLASS_STUDENTS, ARG_FRIENDSHIP_DF):

		# Iterate through the other students in the class
		for i, ops in ARG_OPARKCLASS_STUDENTS.items():

			if i == self.get_id():
				continue

			opf = OParkFriend.OParkFriend(self, ops)
			opf.set_friendship_type(ARG_FRIENDSHIP_DF)

			self.friends.append(opf)
