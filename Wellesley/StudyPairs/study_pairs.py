#import penpyxl
import itertools
import pandas as pd

child_class_file = "By Child Pairs included_excluded 11.13.18.xlsx"

#wb = openpyxl.load_workbook(child_class_file)
#ws = wb["Sheet1"]

child_class_df = pd.read_excel(child_class_file)

name_pair_dict = {}

for class_num in range(1, 11):

    each_classroom = child_class_df[child_class_df["Class"] == class_num]
    classroom_child_names = each_classroom.loc[:, "Name"]
    combs = itertools.product(classroom_child_names, repeat=2)
    for a, b in combs:
        if a == b:
            continue
        out_str = f"{a}-{b}"
        if a > b:
            out_str = f"{b}-{a}"
        if out_str not in name_pair_dict:
            name_pair_dict[out_str] = class_num

# Iterate through each class and form every combination (alphabetize)
