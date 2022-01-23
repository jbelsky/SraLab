#import penpyxl
import itertools
import pandas as pd

child_class_file = "By Child Pairs included_excluded 11.13.18.xlsx"

#wb = openpyxl.load_workbook(child_class_file)
#ws = wb["Sheet1"]

child_class_df = pd.read_excel(child_class_file)

child_dict = {}
name_pair_dict = {}

for class_num in range(1, 11):

    each_classroom = child_class_df[child_class_df["Class"] == class_num]
    classroom_child_names = each_classroom.loc[:, "Name"]
    for child_name in classroom_child_names:
        child_dict[f"{child_name}_{class_num}"] = [0, 0]
    combs = itertools.product(classroom_child_names, repeat=2)
    for a, b in combs:
        if a == b:
            continue
        out_str = f"{a}-{b}"
        if a > b:
            out_str = f"{b}-{a}"
        if out_str not in name_pair_dict:
            name_pair_dict[out_str] = class_num

# Part 1
study_pairs_df = pd.read_excel("Study Pairs 6.25.20.xlsx", skiprows=2, usecols=[2, 3, 7, 8])
pairs = study_pairs_df.loc[~study_pairs_df.iloc[:, 1].isna(), study_pairs_df.columns[1]]
#for pair in study_pairs_df[~study_pairs_df[2].isna(), study_pairs_df[2]]:
#    print(pair)

for child_pair in pairs:
    a, b = child_pair.split("-")
    out_str = child_pair
    if a > b:
        out_str = f"{b}-{a}"
    child_class = name_pair_dict[out_str]
    child_dict[f"{a}_{child_class}"][0] += 1
    child_dict[f"{b}_{child_class}"][0] += 1

pairs2 = study_pairs_df.loc[~study_pairs_df.iloc[:, 3].isna(), study_pairs_df.columns[3]]

for child_pair in pairs2:
    a, b = child_pair.split("-")
    out_str = child_pair
    if a > b:
        out_str = f"{b}-{a}"
    child_class = name_pair_dict[out_str]
    child_dict[f"{b}_{child_class}"][1] += 1

with open("study_pairs_child_cts.txt", mode="w") as fO:
    fO.write("Child Name\tClass Number\tNumber Appear Reciprocal\tNumber Appear Unilateral\n")
    for k, v in child_dict.items():
        # Split the key into name and class
        child_name, class_num = k.split("_")
        fO.write(f"{child_name}\t{class_num}\t{v[0]}\t{v[1]}\n")
