import csv
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent  # folder containing this script

utilities = pd.read_csv(BASE_DIR / "utilities.csv")
substations = pd.read_csv(BASE_DIR / "substations.csv")
lines = pd.read_csv(BASE_DIR / "lines.csv")

valid_ids = set(substations["Substation ID"])
invalid_rows = lines[~lines["Source Substation ID"].isin(valid_ids)]

duplicates = utilities[utilities.duplicated()]
utilities = utilities.drop_duplicates()

irregular_coordinates = substations[
    (substations["Latitude"] < 4)
    | (substations["Latitude"] > 15)
    | (substations["Longitude"] < -17)
    | (substations["Longitude"] > 15)
]

bad_source = lines[~lines["Source Substation ID"].isin(valid_ids)]
bad_dest = lines[~lines["Destination Substation ID"].isin(valid_ids)]

print(f"source refs: {len(bad_source)}")
print(f"destination refs: {len(bad_dest)}")


master_dataset = (
    lines.merge(utilities, on="Utility ID", how="left")
    .merge(
        substations.add_prefix("Source "),
        left_on="Source Substation ID",
        right_on="Source Substation ID",
        how="left",
    )
    .merge(
        substations.add_prefix("Dest "),
        left_on="Destination Substation ID",
        right_on="Dest Substation ID",
        how="left",
    )
)
with open(BASE_DIR / "master_dataset.csv", "w", newline="") as f:
    wr = csv.writer(f)
    for line in master_dataset.itertuples(index=False):
        wr.writerow(line)


foreign_key_relationships = {
    "lines": {
        "Source Substation ID": "substations",
        "Destination Substation ID": "substations",
        "Utility ID": "utilities",
    },
}

valid_ids = set(substations["Substation ID"])
invalid_source_rows = lines[~lines["Source Substation ID"].isin(valid_ids)]
invalid_dest_rows = lines[~lines["Destination Substation ID"].isin(valid_ids)]

substation_lookup_dictionary = substations.set_index("Substation ID").to_dict("index")
utility_lookup_dictionary = utilities.set_index("Utility ID").to_dict("index")

nuber_of_dup_substations = substations["Substation ID"].duplicated().sum()
number_of_dup_utilities = utilities["Utility ID"].duplicated().sum()

no_data_loss = (
    len(lines) == len(master_dataset)
    and master_dataset[["Source Name", "Dest Name", "Name"]].isnull().sum().sum() == 0
    and nuber_of_dup_substations == 0
    and number_of_dup_utilities == 0
)

if no_data_loss:
    print(
        f"CONCLUSION: No data loss detected. All {len(lines)} lines preserved with complete joined data."
    )
else:
    print("CONCLUSION: Data loss or join issues detected")
