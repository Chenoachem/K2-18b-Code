import pandas as pd
import numpy as np

# Load your data
df = pd.read_pickle("signals_dec08_14_not_19.pkl")  # change filename as needed

# Ensure date column is datetime.date
df['date'] = pd.to_datetime(df['date']).dt.date

# Set comparison dates and tolerance
date_08 = pd.to_datetime('2023-12-08').date()
date_14 = pd.to_datetime('2023-12-14').date()
freq_tol = 4e-5  # 4 Hz in MHz

# Filter for the two dates and exclude zero drift rate
df_08 = df[(df['date'] == date_08) & (df['signal_drift_rate'] != 0)]
df_14 = df[(df['date'] == date_14) & (df['signal_drift_rate'] != 0)]

# Extract signal frequencies
freq_08 = df_08['signal_frequency'].values
freq_14 = df_14['signal_frequency'].values

# Find unique-to-Dec-08 frequencies
unique_08_mask = ~np.array([np.any(np.isclose(f, freq_14, atol=freq_tol)) for f in freq_08])
unique_08 = df_08.iloc[unique_08_mask]

# Find unique-to-Dec-14 frequencies
unique_14_mask = ~np.array([np.any(np.isclose(f, freq_08, atol=freq_tol)) for f in freq_14])
unique_14 = df_14.iloc[unique_14_mask]

# Combine the results
df_unique = pd.concat([unique_08, unique_14]).reset_index(drop=True)

# Save the result (optional)
df_unique.to_pickle("unique_signals_08_14_nozerodrift.pkl")
print(f"Saved {len(df_unique)} unique non-zero-drift signals to 'unique_signals_08_14_nozerodrift.pkl'")
