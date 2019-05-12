import openpyxl
from orlandpark import OrlandParkUtils
from orlandpark import classmatrix
from orlandpark import OParkClass

provDir = "C:/usr/GoogleDrive/Programming/SraLab/data/Behavioral Nomination Item data"
behDict = OrlandParkUtils.GetProvisions(provDir)

friendshipMatrixFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/Orland_Park/Friendship_Nominations/Socallb item 5 Unlimited Friend Noms 5.17.17.xlsx"

# Load in the friendship matrix
wb = openpyxl.load_workbook(friendshipMatrixFile)
class_sn = wb.sheetnames
class_sn.sort()

df_stor = []

# Iterate through each class
for cl in class_sn[0:1]:

	print("Getting data for %s..." % cl)

	# Import the nominations matrix
	friendship_df, gender_srs = classmatrix.GetDataMatrix(wb[cl])

	opc = OParkClass.OParkClass(cl)

	opc.initialize_students(gender_srs)

	opc.initialize_provisions(behDict)


#	opc.initialize_friends(friendship_df)

#	clOutput_df = opc.get_friendship_nom_summary()

#	df_stor.append(clOutput_df)


#combinedOutput_df = pd.concat(df_stor)

#combinedOutput_df.to_csv("friendship_nomination_summary_20190228.txt", sep = "\t")
