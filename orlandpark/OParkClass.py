import pandas as pd
import OParkStudent
from collections import OrderedDict

# Set up the new OPClass

class OParkClass:

	def __init__(self, ARG_CLASS_ID):

		self.classID = ARG_CLASS_ID
		self.students = OrderedDict()

	'''
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
	'''

	def get_studentIDs(self):

		return [s.studentID for s in self.students_list]

	def get_studentID(self, _studentID):

		studentID_list = self.get_studentIDs()
		oParkStudent_idx = studentID_list.index(_studentID)

		return self.students_list()[oParkStudent_idx]

	def initialize_students(self, ARG_GENDER_SRS):

		for i, g in ARG_GENDER_SRS.iteritems():

			self.students[i] = OParkStudent.OParkStudent(i, g, self)

	def initialize_friends(self, ARG_FRIENDSHIP_DF):

		for i, ops in self.students.items():

			ops.init_class_friendships(self.students, ARG_FRIENDSHIP_DF)

	def write_friendship_nom_summary(self, outFile):

		fO = open(outFile, mode = "w")

		NEED_HEADER = True

		for i, ops in self.students.items():

			friendshipSummary = ops.get_number_of_friendship_types()
			nominationSummary = ops.get_number_of_nominations()

			if NEED_HEADER:
				fO.write("StudentID\t" + "\t".join(friendshipSummary.index.tolist() + nominationSummary.index.tolist()) + "\n")
				NEED_HEADER = False

			fO.write(str(i) + "\t" + "\t".join([str(x) for x in friendshipSummary] + [str(x) for x in nominationSummary]) + "\n")

		fO.close()




	def get_student_genders(self):

		return pd.Series(index = self.get_studentIDs(),
                         data = [s.gender for s in self.students_list],
						 dtype = int
                        )

	def get_friendship_genders(self, _studentID):

		friendshipGenders = pd.Series(index = self.get_studentIDs(),
                                      data = [s.gender for s in self.students_list],
                                      dtype = int
                                     )

		# Remove the current student
		return friendshipGenders.drop(index = _studentID)

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

	def get_friendship_srs(self, _studentID):
		return self.friendships_dict[_studentID]

	def set_item_summary(self):

		# Initialize the OrderedDict
		item_odict = OrderedDict()

		# Set the columnNames
		columnNames = self.students_list[0].metricByItem_df.columns

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
