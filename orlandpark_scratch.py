# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 18:39:23 2018

@author: jab112
"""

import openpyxl
import pandas as pd
import numpy as np
import os
import sys
import glob
import argparse
import re
from collections import OrderedDict

from orlandpark import classmatrix
from orlandpark import OParkClass
from orlandpark import OParkStudent
from orlandpark import OParkFriend
from orlandpark import OrlandParkUtils

#provDir = "C:/usr/GoogleDrive/Programming/SraLab/data/Behavioral Nomination Item data"
#tmp_dir = OrlandParkUtils.GetProvisions(provDir)


friendshipMatrixFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/Orland_Park/Friendship_Nominations/Socallb item 5 Unlimited Friend Noms 5.17.17.xlsx"

# Load in the friendship matrix
wb = openpyxl.load_workbook(friendshipMatrixFile)
class_sn = wb.sheetnames
class_sn.sort()

df_stor = []

# Iterate through each class
for cl in class_sn:

	print("Getting data for %s..." % cl)

	# Import the nominations matrix
	friendship_df, gender_srs = classmatrix.GetDataMatrix(wb[cl])

	opc = OParkClass.OParkClass(cl)

	opc.initialize_students(gender_srs)
	opc.initialize_friends(friendship_df)

	clOutput_df = opc.get_friendship_nom_summary()

	df_stor.append(clOutput_df)


combinedOutput_df = pd.concat(df_stor)

combinedOutput_df.to_csv("friendship_nomination_summary_20190228.txt", sep = "\t")
