import pandas as pd
import numpy as np

# Define file paths
BILL_FILE = "../datasets/bills.csv"
LEGISLATOR_FILE = "../datasets/legislators.csv"
VOTE_RESULTS_FILE = "../datasets/vote_results.csv"
VOTES_FILE = "../datasets/votes.csv"

# Read CSV files into DataFrames
bills_df = pd.read_csv(BILL_FILE)
legislators_df = pd.read_csv(LEGISLATOR_FILE)
vote_results_df = pd.read_csv(VOTE_RESULTS_FILE)
votes_df = pd.read_csv(VOTES_FILE)

# Merge vote_results_df with legislators_df on legislator_id
vote_results_with_legislators_df = pd.merge(
    vote_results_df,
    legislators_df,
    left_on="legislator_id",
    right_on="id",
    how="left"
)

# Group by legislator_id, name, and vote_type, and count the number of vote_types
legislator_counts_df = (
    vote_results_with_legislators_df.groupby(["legislator_id", "name", "vote_type"])["vote_type"]
    .count()
    .reset_index(name="vote_count")
)

# Pivot the table so that vote_types become columns
legislator_counts_df = pd.pivot_table(
    legislator_counts_df,
    index=["legislator_id", "name"],
    columns="vote_type",
    values="vote_count",
    aggfunc=np.sum,
).reset_index()

# Rename the columns to be more descriptive
legislator_counts_df = legislator_counts_df.rename(
    columns={1: "num_supported_bills", 2: "num_opposed_bills"}
)

# Write the resulting DataFrame to a CSV file
legislator_counts_df.to_csv("../outputs/legislators-support-oppose-count.csv", index=False)
