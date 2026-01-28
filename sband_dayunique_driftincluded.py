import pandas as pd
from astropy.time import Time
from tqdm import tqdm

df = pd.read_pickle("k218b_unique_signals_s-band_2.pkl")

# Create datetime/date columns from MJD
t = Time(df['tstart'].values, format='mjd')
df['datetime'] = t.to_datetime()
df['date'] = [dt.date() for dt in t.to_datetime()]

# Define the three dates of interest
date_03 = pd.to_datetime('2023-10-03').date()
date_05 = pd.to_datetime('2023-10-05').date()
date_13 = pd.to_datetime('2023-10-13').date()
date_08 = pd.to_datetime('2023-12-08').date()
date_14 = pd.to_datetime('2023-12-14').date()
date_21 = pd.to_datetime('2023-12-21').date()
target_dates = [date_03,date_05,date_13,date_08, date_14, date_21]

# Keep only rows from the target days
df = df[df['date'].isin(target_dates)].copy()

# Frequency tolerance in Hz
TOL = 2E-6

unique_rows = []

# Loop over each day with a progress bar
for current_date, df_day in tqdm(df.groupby('date'), desc="Processing days"):
    # All signals from *other* days
    df_other = df[df['date'] != current_date]

    # If there are no other days (safety check)
    if df_other.empty:
        unique_rows.append(df_day)
        continue

    # Collect unique indices for this day
    unique_idx_day = []

    # --- NEW: group by drift rate and only compare within same drift ---
    for drift_rate, df_day_drift in df_day.groupby('signal_drift_rate'):
        df_other_drift = df_other[df_other['signal_drift_rate'] == drift_rate]

        # If no signals on other days with this drift rate, keep them all
        if df_other_drift.empty:
            unique_idx_day.extend(df_day_drift.index.tolist())
            continue

        # Prepare left/right for merge_asof
        left = df_day_drift[['signal_frequency']].copy()
        left = left.sort_values('signal_frequency')
        left['orig_index'] = left.index

        right = df_other_drift[['signal_frequency']].copy()
        right = right.sort_values('signal_frequency')
        right = right.rename(columns={'signal_frequency': 'signal_frequency_other'})

        # Align each signal with the nearest frequency from other days
        merged = pd.merge_asof(
            left,
            right,
            left_on='signal_frequency',
            right_on='signal_frequency_other',
            direction='nearest'
        )

        # A "duplicate" is: same drift_rate (by construction of the group)
        # AND frequency within ±TOL Hz on another day
        has_close_match = (
            merged['signal_frequency_other'].notna() &
            (merged['signal_frequency'] - merged['signal_frequency_other']).abs() <= TOL
        )

        # Unique signals are those without any close freq match at same drift_rate
        unique_indices = merged.loc[~has_close_match, 'orig_index']
        unique_idx_day.extend(unique_indices.tolist())

    # Add this day's unique rows
    unique_rows.append(df_day.loc[unique_idx_day])

# Combine and sort final results
result = pd.concat(unique_rows).sort_values(['date', 'signal_frequency'])

# Save result
outfile = "signals_unique_across_3days_tol2Hz_by_drift.pkl"
result.to_pickle(outfile)
print(f"Saved {len(result)} unique signals across 3 days to '{outfile}'")

