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

print(f"Orphaned source refs: {len(bad_source)}")
print(f"Orphaned destination refs: {len(bad_dest)}")
