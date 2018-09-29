# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:16:15 2018

@author: jab112
"""

import openpyxl
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_excel", help = "the input Socalla Excel sheet")
# parser.add_argument("output_text", help = "the output text file")
args = parser.parse_args()
wb = openpyxl.load_workbook(args.input_excel)

#for i in range(15, 53):
for i in range(15, 16):

	sheet_name = "Class " + str(i)
	print(sheet_name)
	ws = wb[sheet_name]

	# Find the indices
	columnA = np.array([c.value for c in ws["A"]])
	iStuIDs = np.where(~((columnA == None) | (columnA == "ID")))[0]
	stuIDs = pd.Index(columnA[iStuIDs])

	# Get the gender (Column B)
	iStart = iStuIDs[0]
	iEnd = iStuIDs[-1]
	genders = pd.Series([c.value for c in ws["B"][iStart:(iEnd + 1)]], index = stuIDs, dtype = np.int16)

	# Create the pandas 2-D matrix
	score_matrix = []
	for r in ws.iter_rows(min_row = iStart + 1, max_row = iEnd + 1, min_col = iStart + 1, max_col = iEnd + 1):
		score_matrix.append([c.value for c in r])
	score_df = pd.DataFrame(score_matrix, index = stuIDs, columns = stuIDs, dtype = np.int16)

	# Construct the output dataframe
	output_df = pd.DataFrame(np.column_stack((stuIDs, genders)),
								  columns = ["StudentID", "Gender"],
								  index = stuIDs
							 )

	# Add in the additional columns
	addl_columns = ["Given_mean", "Given_ClassGender_mean", "Given_ClassGender_std", "Given_ClassGender_zscore",
					   "Received_mean", "Received_ClassGender_mean", "Received_ClassGender_std", "Received_ClassGender_zscore"
				     ]
	output_df = output_df.reindex(columns = output_df.columns.tolist() + addl_columns, fill_value = 0)

	# Need to patch colA, gender_idx, output_df, and df if any of the
	STUDENT_IDS_SKIP = [2309, 2707, 2708, 4114, 4124, 4621, 4819]
	if any(stuIDs.isin(STUDENT_IDS_SKIP)):
		stuID_drop = stuIDs[stuIDs.isin(STUDENT_IDS_SKIP)]
		output_df.drop(stuID_drop, inplace = True)
		score_df.drop(index = stuID_drop, columns = stuID_drop, inplace = True)

	# Create the output for each type [AllGender, ByGender, CrossGender]
	output_template = output_df.copy()

	# Iterate through each id
	for stuID in output_df.index:

		# Get the given and received score
		givenScore = score_df.loc[studentID]
		receiveScore = score_df[studentID]

		# Get scores != 9
		iGiven = givenScore != 9
		iReceive = receiveScore != 9

		# See if there needs to be a gender filter
		if analysisType == "ByGender":
			iGiven = iGiven & (genders == output_df.loc[stuID, "Gender"])
			iReceive = iGiven & (genders == output_df.loc[stuID, "Gender"])
		elif analysisType == "CrossGender":
			iGiven = iGiven & (genders != output_df.loc[stuID, "Gender"])
			iReceive = iGiven & (genders != output_df.loc[stuID, "Gender"])

		# Subset on the score
		score = score[scoreSubset_idx]

		if len(score) > 0:
			meanScore = score.mean()
		else:
			meanScore = 9

		# Select the output column
		output_df.loc[output_df["StudentID"] == studentID, colname] = meanScore

	# Get the class-gender mean and std
	for g in [0, 1]:

		for gr in ["Given", "Received"]:

			# Set the idx
			idx = (output_df["Gender"] == g) & (output_df[gr + "_mean"] != 9)

			output_df.loc[idx, gr + "_ClassGender_mean"] = output_df.loc[idx, gr + "_mean"].mean()
			output_df.loc[idx, gr + "_ClassGender_std"] = output_df.loc[idx, gr + "_mean"].std()

			# Set the missing means and std to 9
			idx = (output_df["Gender"] == g) & (output_df[gr + "_mean"] == 9)
			output_df.loc[idx, gr + "_ClassGender_mean"] = 9
			output_df.loc[idx, gr + "_ClassGender_std"] = 9


	# Set the missings to 9!
	# Get rid of the chain indexing from below


	for stIdx in output_df.index:

		for gr in ["Given", "Received"]:

			# Calculate z-score
			curMean = output_df.loc[stIdx, gr + "_mean"]
			classMean = output_df.loc[stIdx, gr + "_ClassGender_mean"]
			stDev = output_df.loc[stIdx, gr + "_ClassGender_std"]

			#if sheet_name == "Class 23":
			#	print(str(output_df.loc[stIdx, "StudentID"]) + "\t" + "\t".join([str(curMean),str(classMean),str(stDev)]))

			# Get the z_score if not missing
			if curMean == 9:
				z_score = 9
			else:
				z_score = (curMean - classMean) / stDev

			output_df.loc[stIdx,gr + "_ClassGender_zscore"] = z_score

	if sheet_name == "Class 15":
		output_df.to_csv(args.output_text, mode = "w", sep = "\t", header = True, index = False)
	else:
		output_df.to_csv(args.output_text, mode = "a", sep = "\t", header = False, index = False)

'''