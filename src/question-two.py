import pandas as pd

# Define file paths
BILLS_PATH = "../datasets/bills.csv"
LEGISLATORS_PATH = "../datasets/legislators.csv"
VOTE_RESULTS_PATH = "../datasets/vote_results.csv"
VOTES_PATH = "../datasets/votes.csv"

# Load CSV files into DataFrames
bills_df = pd.read_csv(BILLS_PATH)
legislators_df = pd.read_csv(LEGISLATORS_PATH)
vote_results_df = pd.read_csv(VOTE_RESULTS_PATH)
votes_df = pd.read_csv(VOTES_PATH)

# Merge bills and legislators DataFrames
bills_with_legislators_df = pd.merge(
    bills_df, legislators_df, left_on="sponsor_id", right_on="id", how="left"
)

# Rename column name to primary_sponsor
bills_with_legislators_df = bills_with_legislators_df.rename(
    columns={"name": "primary_sponsor"}
)

# Fill NA/NaN values with "Unknown"
bills_with_legislators_df = bills_with_legislators_df.fillna("Unknown")

# Merge bills and votes DataFrames, then rename columns
bills_with_legislators_and_votes_df = pd.merge(
    bills_with_legislators_df,
    votes_df,
    left_on="id_x",
    right_on="bill_id",
    how="left",
).rename(columns={'id_x' : 'id_billcsv', 'id_y' : 'id_legislatorcsv', 'id' : 'id_votescsv'})


# Merge with vote results DataFrame
bills_with_legislators_and_votes_with_vote_results_df = pd.merge(
    bills_with_legislators_and_votes_df,
    vote_results_df,
    left_on="id_votescsv",
    right_on="vote_id",
    how="left",
)

# Group by bill attributes and vote type, count votes, and pivot to wide format
bill_counts_df = (
    bills_with_legislators_and_votes_with_vote_results_df.groupby(
        ["bill_id", "vote_type", "title", "primary_sponsor"]
    )["id"]
    .count()
    .reset_index()
    .pivot_table(
        index=["bill_id", "title", "primary_sponsor"],
        columns="vote_type",
        values="id",
    )
    .reset_index()
)

# Rename columns and write to CSV file
bill_counts_df = bill_counts_df.rename(
    columns={1: "supporter_count", 2: "opposer_count"}
)

bill_counts_df.to_csv("../outputs/bills.csv", index=False)
