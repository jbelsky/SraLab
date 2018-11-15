# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 17:07:00 2018

@author: BelskyJ
"""

import openpyxl
import pandas as pd
import numpy as np
import os
import glob

import classmatrix

# Load in the friendship matrix
f_xls = "c:/usr/opt/cygwin64/home/belskyj/JAB_GitHub/SraLab/data/Orland_Park/Friendship_Nominations/Socallb item 5 Unlimited Friend Noms 5.17.17.xlsx"

wb = openpyxl.load_workbook(f_xls)
ws = wb["Class 15"]

friendship_df, gender_s = classmatrix.GetDataMatrix(ws)

given = friendship_df.iloc[:,0]
received = friendship_df.iloc[0]
friendship_status = []

for i,v in given.iteritems():
	print(str(i) + "\t" + str(v))

# Get the friendship status

# Load in the peer provisions
peerProv_xls_files = glob.glob("c:/usr/opt/cygwin64/home/belskyj/JAB_GitHub/SraLab/data/Orland_Park/Peer_Provisions/*.xlsx")
peerProv_xls_files.sort()
for pp_xls in peerProv_xls_files:

	pp_wb = openpyxl.load_workbook(pp_xls)

	for sheet_name in pp_wb.sheetnames:
			
		if "Class" not in sheet_name:
			continue
		
		print("%s\t%s" % (os.path.basename(pp_xls), sheet_name))
		
		data_df, gender_s = classmatrix.GetDataMatrix(wb[sheet_name])
		
		break
	
	break