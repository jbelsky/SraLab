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

import classmatrix
import OParkClass
import OParkStudent
import OParkFriend
import OrlandParkUtils

friendshipMatrixFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/Orland_Park/Friendship_Nominations/Socallb item 5 Unlimited Friend Noms 5.17.17.xlsx"

# Load in the friendship matrix
wb = openpyxl.load_workbook(friendshipMatrixFile)
class_sn = wb.sheetnames
class_sn.sort()

df_stor = []

# Iterate through each class
for cl in class_sn:

	

	# Import the nominations matrix
	friendship_df, gender_srs = classmatrix.GetDataMatrix(wb[cl])

	opc15 = OParkClass.OParkClass(cl)

	opc15.initialize_students(gender_srs)
	opc15.initialize_friends(friendship_df)
	my_df = opc15.get_friendship_nom_summary()
	df_stor.append(my_df)

'''
stID = list(friendship_dict.keys())
stID.sort()

for s in stID:

	st_df = friendship_dict[s]
	frTypes = st_df["Type"].value_counts()
	fr_d = {}

	for t in ["reciprocated", "given", "received", "none", "NA"]:

		if t in frTypes.index:
			fr_d[t] = frTypes.loc[t]
		else:
			fr_d[t] = 0

	print("%d\t%d\t%d\t%d\t%d\t%d\n" % (s, fr_d["reciprocated"], fr_d["given"], fr_d["received"], fr_d["none"], fr_d["NA"]))



OParkStudentDict = OrderedDict()
for i in gender_srs.index:

	# Set the OParkStudent list
	OParkStudentDict[i] = OParkStudent.OParkStudent(i, gender_srs.loc[i])

# Set the OParkStudent list
OPstudent_list = [OParkStudent.OParkStudent(i, gender_srs.loc[i]) for i in gender_srs.index]

# Initialize an OPClass
orlandParkClass = OParkClass.OParkClass("Class 15", OPstudent_list, friendship_dict, classPeerProvisionsByItem_dict)

ops = OParkStudentDict[1510]
ops.set_oParkClass(orlandParkClass)
ops.set_received_peerprov_df()
ops.set_received_friendships()
ops.set_provision_received_by_friendship_status()

ops.set_provision_stats()

for i in range(1, 13):
	for f in ["reciprocated", "given", "received", "none"]:
		for g in [0, 1, 9]:
			a = ops.get_friendship_prov_gender(f, g, "sameGender", i)
			b = ops.get_friendship_prov_gender(f, g, "crossGender", i)
			c = a + b
			print("%s:\t%d\t%d\t%d" % (f + "," + str(g), a, b, c))
'''
