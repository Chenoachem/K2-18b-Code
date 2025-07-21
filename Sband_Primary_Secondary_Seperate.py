import pandas as pd
from astropy.time import Time

# Load data
df = pd.read_pickle("k218b_unique_signals_s-band.pkl")

# Convert MJD to datetime and split into date/time
t = Time(df['tstart'].values, format='mjd')
df['datetime'] = t.to_datetime()
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

# Define the Secondary observation windows
secondary_ranges = [
    (pd.to_datetime('2023-09-26').date(), pd.to_datetime('2023-10-12').date()),
    (pd.to_datetime('2023-10-28').date(), pd.to_datetime('2023-11-13').date()),
    (pd.to_datetime('2023-11-30').date(), pd.to_datetime('2023-12-16').date()),
]

# Function to check if a date is in any of the ranges
def is_secondary(date):
    return any(start <= date <= end for start, end in secondary_ranges)

# Apply function to create a mask
df['is_secondary'] = df['date'].apply(is_secondary)

# Split into two dataframes
df_secondary = df[df['is_secondary']].copy()
df_primary = df[~df['is_secondary']].copy()

# Optional: drop the helper column
df_secondary.drop(columns=['is_secondary'], inplace=True)
df_primary.drop(columns=['is_secondary'], inplace=True)

# Save both dataframes to pickle files
df_secondary.to_pickle("secondary_signals.pkl")
df_primary.to_pickle("primary_signals.pkl")

# Summary printout
print(f"Saved {len(df_secondary)} rows to 'secondary_signals.pkl'")
print(f"Saved {len(df_primary)} rows to 'primary_signals.pkl'")

