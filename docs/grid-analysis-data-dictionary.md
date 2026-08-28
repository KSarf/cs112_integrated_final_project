# Grid Analysis Data Dictionary

## utilities.csv

| Field | Meaning |
|---|---|
| Utility ID | Unique utility identifier |
| Name | Full utility name |
| Alias | Common utility abbreviation |
| Code | Short utility code |
| Type | Distribution, transmission or generation |
| Country | Utility location |
| Active | Whether the utility is marked active |

## substations.csv

| Field | Meaning |
|---|---|
| Substation ID | Unique substation identifier |
| Name | Full substation name |
| Short Name | Short location name |
| Region | Region or cross-border area |
| Country | Country |
| Latitude | Approximate latitude |
| Longitude | Approximate longitude |
| Voltage (kV) | Substation voltage rating |
| Capacity (MVA) | Approximate capacity |
| Commissioning Year | Approximate commissioning year |
| Type | Distribution, bulk supply point or transmission |
| Status | Active or inactive |

## lines.csv

| Field | Meaning |
|---|---|
| Line ID | Unique line identifier |
| Utility ID | Foreign key to utilities |
| Source Substation ID | Foreign key to source substation |
| Source Substation | Source name |
| Destination Substation ID | Foreign key to destination substation |
| Destination Substation | Destination name |
| Voltage (kV) | Line voltage |
| Length (km) | Approximate line length |
| Capacity (MVA) | Approximate line capacity |
| Status | Active or under maintenance |
| Line Type | Overhead or underground |

## Main Relationships

- `lines.Utility ID` references `utilities.Utility ID`.
- `lines.Source Substation ID` references `substations.Substation ID`.
- `lines.Destination Substation ID` references `substations.Substation ID`.
