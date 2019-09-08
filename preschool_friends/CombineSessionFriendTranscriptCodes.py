import openpyxl
import pandas as pd
from collections import OrderedDict

from pandas import DataFrame

inputFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/preschool_friends/FriendTranscriptCodes 9.7.19.xlsx"

# Open the file
wb = openpyxl.load_workbook(inputFile)
ws = wb[wb.sheetnames[0]]

# Convert to df
data_df = pd.DataFrame(ws.values) # type: DataFrame

# Get the rowname and column names
colNames = data_df.iloc[1, 1:]
rowNames = data_df.iloc[2:, 0]

# Subset on the data
data_df = data_df.iloc[2:, 1:]
data_df.index = rowNames
data_df.columns = colNames

# Drop the 1st two metadata columns
dataSubset_df = data_df.iloc[:, 2:]

# Find the mapping of column idx to column name in both sessions
s1 = OrderedDict()
s2 = OrderedDict()

# Begin in 3rd column
isSession1 = True
for i, v in enumerate(dataSubset_df.columns[:]):

	if isSession1:
		if v in s1:
			isSession1 = False
			s2[v] = i
		else:
			s1[v] = i

	else:
		if v in s2:
			break
		else:
			s2[v] = i

# Ensure that the keys in each session are equivalent
if len(s1.keys()) != len(s2.keys()):
	raise ValueError("Session1 has %d columns but Session3 has %d columns" % (len(s1.keys()), len(s2.keys())))

elif s1.keys() != s2.keys():

	# If they aren't print out the differences
	s1Keys = list(s1.keys())
	s2Keys = list(s2.keys())

	print("\tSession1\tSession3")
	print("\t--------\t--------")

	for i in range(len(s1Keys)):

		s1Val = s1Keys[i]
		s2Val = s2Keys[i]

		if s1Val != s2Val:

			print("\t" + s1Val + "\t" + s2Val)

	raise ValueError("Session1 and Session3 have different column names!")

# Create the output data frame
output_df = pd.DataFrame(index = dataSubset_df.index, columns = s1.keys())

# Iterate through each column
for colName in output_df.columns:

	for stID in output_df.index:

		# Get the s1 and s3 values
		s1Val = dataSubset_df.loc[stID].iloc[s1[colName]]
		s2Val = dataSubset_df.loc[stID].iloc[s2[colName]]

		# Set the combined number
		outVal = 0
		if s1Val == 1 and s2Val == 0:
			outVal = 1
		elif s1Val == 0 and s2Val == 1:
			outVal = 3
		elif s1Val == 1 and s2Val == 1:
			outVal = 2

		# Enter the outVal into the output_df
		output_df.loc[stID, colName] = outVal

# Write the output
outputFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/preschool_friends/combined_files.txt"
output_df.to_csv(outputFile, sep = "\t", index = True, index_label = "StudentID", header = True)
