import openpyxl
import pandas as pd
import itertools
from collections import OrderedDict

inputFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/Orland_Park/OP Missing Data.xlsx"

# Open the file
wb = openpyxl.load_workbook(inputFile)
ws = wb[wb.sheetnames[0]]

# Convert to df
data_df = pd.DataFrame(ws.values)
data_df.columns = data_df.loc[0]
data_df = data_df.iloc[1:]
data_df.index = data_df["id"]
data_df = data_df.iloc[:, 1:]

# Create the missing pairs
cols = data_df.columns
missingPairs = OrderedDict()

for i in range(0, len(cols)):

        for j in itertools.combinations(cols, i + 1):

            missingPairs[j] = 0

# Iterate through the first 20 rows
for r, v in data_df.iterrows():

    # Obtain the logical vector of None or 99
    missing = v.isnull() | (v == 99)

    if any(missing):

        # Get the missing columns
        missCols = tuple(cols[missing])

        # Add a tally to the missing pairs
        missingPairs[missCols] += 1

# Write the output
outputFile = "C:/Programs/cygwin64/home/jab112/github/SraLab/data/output/missing_data_columns.txt"
fO = open(outputFile, mode = "w")
fO.write("MissingColumns\tCount\n")
for k, v in missingPairs.items():

    if v > 0:

        fO.write("; ".join(k) + "\t" + str(v) + "\n")

fO.close()
