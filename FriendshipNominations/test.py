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

pobj = p_dict[192392]

for k, v in pobj.get_nominations().items():
    if k not in p_dict:
        print(str(k) + "\t" + "9")
    else:
        print(pobj.check_reciprocal_friend(p_dict[k]))
        print(pobj.check_reciprocal_top3(p_dict[k]))
        print(pobj.check_reciprocal_closest(p_dict[k]))
