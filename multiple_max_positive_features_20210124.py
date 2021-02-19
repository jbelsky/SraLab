import itertools
import pandas as pd
import numpy as np
import re
import sys

def get_friend_index(scores, max_score):

    # Create an np.array of the scores
    scores = np.array(scores)
    num_nan_scores = len(np.isnan(scores).nonzero()[0])

    if num_nan_scores > 1 and np.isnan(max_score):
        return np.NaN
    elif all(np.isnan(scores)):
        print(f"Max score is {max_score} but scores are not all np.NaN!")
        return -1
    elif np.isnan(max_score) and num_nan_scores < 2:
        print(f"Max score is np.NaN but not all scores are np.NaN!")
        return -2

    # Otherwise, find the index of the max score
    max_score_idx = np.nonzero(scores == max_score)[0]
    max_score_idx += 1

    if len(max_score_idx) > 1:
        return "".join([str(x) for x in max_score_idx])
    else:
        return max_score_idx[0]


# Read in the csv file
scores_df = pd.read_csv("Multiple Max Positive Features 1.24.21.csv", index_col=0, na_values=[-9, "", " "])

# Extract out the metric from the column name
# 11 metrics of form F[123]FFQ_([A-Za-z]{1,3})Avg
p = re.compile("F[123]FFQ_([A-Za-z]{1,3})Avg")
metrics = []
for colname in scores_df.columns[0:11]:
    m = p.match(colname)
    try:
        metrics.append(m.group(1))
    except AttributeError:
        print(f"Could not extract metric from column name {colname}, exiting...")
        sys.exit(1)

# Create the column names for the output_df
colnames_out = []
for metric in metrics:
    # Suffix metric with "Friends"
    metric_with_suffix = metric + "Friends"

    # Prefix "Min" and "Max" to colnames
    colnames_out.append("Min" + metric_with_suffix)
    colnames_out.append("Max" + metric_with_suffix)

# Make the output df
out_df = pd.DataFrame(index=scores_df.index, columns=colnames_out)

'''
# Iterate through each row
for id, vals in max_scores_df.iterrows():

    col_idx = 0

    # Iterate through each of the columns
    for col in out_df.columns:

        # Get the return val
        val = get_friend_index(vals.iloc[col_idx:(col_idx + 3)], vals[col])

        # Insert into the out_df
        out_df.loc[id, col] = val

        # Iterate the column index
        col_idx += 3

out_df.to_csv("max_scores.txt", sep="\t", na_rep=-9)
'''