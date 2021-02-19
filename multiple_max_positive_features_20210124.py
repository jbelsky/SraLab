import itertools
import pandas as pd
import numpy as np
import re
import sys

def get_friend_index(row, metric_name):

    # Get the scores for each friend
    friends_scores = get_friend_metrics(row, metric_name)

    # Create an np.array of the scores
    scores = np.array(friends_scores)

    # Get the friend(s) with the minimum score
    friend_min = get_friend_subset(scores, row["Min" + metric_name])
    friend_max = get_friend_subset(scores, row["Max" + metric_name])

    return friend_min, friend_max


def get_friend_subset(friend_scores, value):

    num_nan_scores = len(np.isnan(friend_scores).nonzero()[0])

    if num_nan_scores > 1 and np.isnan(value):
        return np.NaN
    elif all(np.isnan(friend_scores)):
        print(f"Min/Max score is {value} but scores are not all np.NaN!")
        return -1
    elif np.isnan(value) and num_nan_scores < 2:
        print(f"Min/Max score is np.NaN but not all scores are np.NaN!")
        return -2

    # Otherwise, find the index of the minmax score
    score_idx = np.nonzero(friend_scores == value)[0]
    score_idx += 1

    if len(score_idx) > 1:
        return "".join([str(x) for x in score_idx])
    else:
        return score_idx[0]




def get_friend_metrics(row, metric_name):

    # Create the list
    metric_list = []

    # Append each friend score to the list
    for friend in [1, 2, 3]:
        colname = f"F{friend}FFQ_{metric_name}Avg"
        value = row[colname]
        metric_list.append(value)

    return metric_list



# Read in the csv file
scores_df = pd.read_csv("Multiple Max Positive Features 1.24.21.csv", index_col=0, na_values=[-9, "", " "])

# Extract out the metric from the column name
# 11 metrics of form F[123]FFQ_([A-Za-z]{1,3})Avg
p = re.compile("F[123]FFQ_([A-Za-z]{1,3})Avg")
metrics = []
for colname in scores_df.columns[0:11]:
    m = p.match(colname)
    try:

        # Get the metric
        metric = m.group(1)

        # Don't have M[in|ax][SA|C]
        if metric not in ["SA", "C"]:
            metrics.append(metric)

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

# Iterate through each row
for id, vals in scores_df.iterrows():

    # Iterate through each of the columns
    for metric in metrics:

        # Get the return val
        fr_min, fr_max = get_friend_index(vals, metric)

        # Insert into the out_df
        out_df.loc[id, "Min" + metric + "Friends"] = fr_min
        out_df.loc[id, "Max" + metric + "Friends"] = fr_max

out_df.to_csv("multiple_max_positive_features.txt", sep="\t", na_rep=-9)