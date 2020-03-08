import openpyxl
from person import Person

data_file = "sample Friend Noms 2.27.20.xlsx"

# Open the xls document
wb = openpyxl.load_workbook(data_file)

# Assume only one sheet
ws = wb.active

# Get the header
header = [x.value for x in ws[1]]

# Initialize the person dict
p_dict = {}

# Iterate through each person
for r in ws.iter_rows(min_row=2):

    # Skip line if blank
    if not r[0].value:
        continue

    # Get the row into a list
    row_list = [v.value for v in r]

    p = Person(row_list[0])

    p.add_nominations(row_list)

    p_dict[p.id] = p
