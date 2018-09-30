# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:16:15 2018

Updated: 2018-09-30

@author: jab112
"""

import openpyxl
import pandas as pd
import numpy as np
import argparse
import itertools
from collections import OrderedDict

def GetStuAvgScore(arg_out_df, arg_score_df, arg_id, arg_gender, arg_type):

	# Get the given or received score
	score = pd.Series(dtype = np.int64)
	if arg_type == "Given":
		score = arg_score_df.loc[arg_id]
	elif arg_type == "Received":
		score = arg_score_df[arg_id]

	# Get scores != 9
	# See if there needs to be a gender filter
	iScore = score != 9
	if arg_gender == "ByGender":
		iScore = iScore & (arg_out_df["Gender"] == arg_out_df.loc[arg_id, "Gender"])
	elif arg_gender == "CrossGender":
		iScore = iScore & (arg_out_df["Gender"] != arg_out_df.loc[arg_id, "Gender"])

	# Subset on the score
	score = score[iScore]
	scoreMean = score.mean() if len(score) > 0 else 9

	arg_out_df.loc[arg_id, "mean"] = scoreMean

def GetClassAvgScore(arg_out_df):

	# Obtain the indices where there is a mean
	iScore = arg_out_df["mean"] != 9

	# Set no mean score std and mean to 9
	if any(~iScore):
		arg_out_df.loc[~iScore, "ClassGender_mean"] = 9
		arg_out_df.loc[~iScore, "ClassGender_std"] = 9

	# Iterate through each gender separately
	for g in arg_out_df["Gender"].unique():

		# Get the iScore Gender
		iGender = arg_out_df["Gender"] == g
		iScoreGender = iScore & iGender

		arg_out_df.loc[iScoreGender, "ClassGender_mean"] = arg_out_df.loc[iScoreGender,"mean"].mean()
		arg_out_df.loc[iScoreGender, "ClassGender_std"] = arg_out_df.loc[iScoreGender,"mean"].std()

def GetZscore(row):

	if row["mean"] == 9:
		return 9

	return (row["mean"] - row["ClassGender_mean"]) / row["ClassGender_std"]

parser = argparse.ArgumentParser()
parser.add_argument("input_excel", help = "the input Socalla Excel sheet")
parser.add_argument("output_text", help = "the output text file")
args = parser.parse_args()
wb = openpyxl.load_workbook(args.input_excel)

data_d = OrderedDict()

#for i in range(15, 53):
for sheet_name in wb.get_sheet_names():

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
	outTemplate_df = pd.DataFrame(genders,
								      columns = ["Gender"],
									   index = stuIDs
								      )

	# Add in the additional columns
	addl_columns = ["mean", "ClassGender_mean", "ClassGender_std", "ClassGender_zscore"]
	outTemplate_df = outTemplate_df.reindex(columns = outTemplate_df.columns.tolist() + addl_columns, fill_value = 0)

	# Need to patch colA, gender_idx, output_df, and df if any of the
	STUDENT_IDS_SKIP = [2309, 2707, 2708, 4114, 4124, 4621, 4819]
	if any(stuIDs.isin(STUDENT_IDS_SKIP)):
		stuID_drop = stuIDs[stuIDs.isin(STUDENT_IDS_SKIP)]
		outTemplate_df.drop(stuID_drop, inplace = True)
		score_df.drop(index = stuID_drop, columns = stuID_drop, inplace = True)

	# Ensure that there aren't any unknown genders
	if(any(~outTemplate_df["Gender"].isin([0,1]))):
		iUnknownGender = ~outTemplate_df["Gender"].isin([0,1])
		for s in outTemplate_df.index[np.where(iUnknownGender)[0]]:
			print("ERROR: %d gender is %d (must be '0' or '1')!" % (s, outTemplate_df.loc[s,"Gender"]))
		break

	# Create the output for each type [AllGender, ByGender, CrossGender]
	genderComps = ["AllGender", "ByGender", "CrossGender"]
	analysisTypes = ["Given", "Received"]

	for gComp, aType in itertools.product(genderComps, analysisTypes):

		output_df = outTemplate_df.copy()

		# Get the average score for each student
		for stuID in output_df.index:

			# Get the student average score
			GetStuAvgScore(output_df, score_df, stuID, gComp, aType)

		# Get the class gender mean and std (stratified by gender)
		GetClassAvgScore(output_df)

		# Convert to z-score
		output_df["ClassGender_zscore" ] = output_df.apply(GetZscore, axis = 1)

		# Store in data dict
		key = (gComp, aType)
		if key not in data_d:
			data_d[key] = output_df
		else:
			data_d[key] = data_d[key].append(output_df)

# Create the output workbook
writer= pd.ExcelWriter(args.output_text)
for k in data_d.keys():
	data_d[k].to_excel(writer, sheet_name = "_".join(k))

writer.save()