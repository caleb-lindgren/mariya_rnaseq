import glob
import os
import pandas as pd
import sys

# Usage: python 01_clean_data.py PATH/TO/DIRECTORY/WITH/MARIYA/RNASEQ/FILES/

input_dir = sys.argv[1]

# Get all the filenames from the data folder that start with "A375_Day"
paths = pd.Series(glob.glob(f"{input_dir}/A375_Day*"))

# Read in all those files and join them together into one combined table
all_days = pd.DataFrame(columns=["HUGO"])
for path in paths:

    day = int(path.split("Day", 1)[1].split("VS", 1)[0])

    day_df = pd.read_csv(path)

    day_df = pd.\
    read_csv(path)[["HUGO", "log2FoldChange"]].\
    drop_duplicates(keep="first")

    # These tables were put through Excel at some point and it messed up column
    # names, so let's fix that
    day_df = day_df.assign(
        HUGO=day_df.HUGO.replace({
            "1-Mar": "MARCH1",
            "2-Mar": "MARCH2",
            "9-Mar": "MARCH9",
            "3-Sep": "SEPT3",
            "8-Sep": "SEPT8",
            "9-Sep": "SEPT9",
            "11-Sep": "SEPT11",
        }),
    )

    # Make sure the column name for each individual day tells what day it is
    day_df = day_df.rename(columns={"log2FoldChange": day})

    all_days = all_days.merge(
        right=day_df,
        on="HUGO",
        how="outer",
    )

# A mythical "Day 131" data file has been created that is just a duplicate of
# the day 250 data. So we'll get rid of that column.
all_days = all_days.drop(columns=131)

# Make HUGO name the index and sort so it looks pretty
all_days = all_days.\
set_index("HUGO").\
sort_index().\
sort_index(axis=1)

# Read in the compiled file--there should be one column in this file that doesn't
# match our data from the individual day files, and that column should be the day 2
# versus day 0 data.
comp = pd.read_csv(f"{input_dir}/A375_Compiled.csv")
comp = comp.drop(columns=comp.columns[comp.columns.str.startswith("Unnamed: ")])

# Group together sets of HUGO name and log2 fold change columns in the compiled data
# folder, since they don't have unique labels
groups = comp.columns.to_series().\
str.split(".", expand=True)[1].\
fillna(0)
groups.name = "group"
groups.index.name = "col"
groups = groups.reset_index()

# Go through and find the column that we don't already have, and add it to our
# all_days table as day 2
not_found = 0
for group in groups.group.unique():
    cols = groups.loc[groups.group == group, "col"]
    sel = comp[cols]
    sel.columns = sel.columns.to_series().str.split(".", expand=True)[0].rename(None)

    # Again, we need to fix some gene names that got converted to dates by Excel
    sel = sel.assign(
        HUGO=sel.HUGO.replace({
            "1-Mar": "MARCH1",
            "2-Mar": "MARCH2",
            "9-Mar": "MARCH9",
            "3-Sep": "SEPT3",
            "8-Sep": "SEPT8",
            "9-Sep": "SEPT9",
            "11-Sep": "SEPT11",
        }),
    ).\
    set_index("HUGO").\
    sort_index()
    joined = sel.join(all_days, how="inner")

    found = False
    for orig_col in all_days.columns:
        # When comparing equality, we have to round to 9 decimal places because the
        # compiled data file apparently had its numbers rounded when it was created.
        if joined["log2FoldChange"].equals(joined[orig_col].round(9)):
            found = True

    if not found:
        # There should only be one unmatched column from the compiled file, and day 2 is
        # the only missing day so we assume the unmatched column is the day 2 data
        not_found += 1
        if not_found != 1:
            raise ValueError(f"Unexpectedly found a second 'not found' group: {group}")

        all_days = sel.\
        rename(columns={"log2FoldChange": 2}).\
        join(all_days, how="outer")

# Add informative text to the column headers
all_days.columns = "day_" + all_days.columns.to_series().astype(str).str.zfill(3) + "_log2fc"

# Save as a TSV (since TSVs are more robust than CSVs)
intermed_dir = "intermediate_files"
all_days.to_csv(f"{intermed_dir}/data_cleaned.tsv", sep="\t", index=True)

# Linecharts showed that day 39 is an outlier for most samples (verified in check_blip.py). We'll exclude it.
all_days = all_days.drop(columns="day_039_log2fc")

# Save .rnk files for GSEA
os.makedirs(f"{intermed_dir}/rnks", exist_ok=True)
for col in all_days.columns:
    all_days[col].dropna().to_csv(f"{intermed_dir}/rnks/{col}.rnk", sep="\t", header=False, index_label=False, index=True)
