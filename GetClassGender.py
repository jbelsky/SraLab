# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:16:15 2018

@author: BelskyJ
"""

import classmatrix
import pandas as pd
import numpy as np
import openpyxl
from collections import OrderedDict

wb = openpyxl.load_workbook("data/Orland_Park/Friendship_Nominations/Socallb item 5 Unlimited Friend Noms 5.17.17.xlsx")
sheetNames = wb.sheetnames
sheetNames.sort()

class_df = OrderedDict()

for c in sheetNames:
	
	if "Class" not in c:
		continue

	data_df, gender_s = classmatrix.GetDataMatrix(wb[c])

	# Get the total number of boys and girls
	girlCt = len(np.where(gender_s == 0)[0])
	boyCt = len(np.where(gender_s == 1)[0])
	
	gender_df = pd.DataFrame(index = gender_s.index,
						     columns = ["Gender", "SameSex", "CrossSex"]
						     )
	gender_df["Gender"] = gender_s
	
	gender_df.loc[gender_df["Gender"] == 0, ["SameSex", "CrossSex"]] = [girlCt, boyCt]
	gender_df.loc[gender_df["Gender"] == 1, ["SameSex", "CrossSex"]] = [boyCt, girlCt]

	class_df[c] = gender_df

out_df = pd.concat(class_df, axis = 0, join = "inner")
