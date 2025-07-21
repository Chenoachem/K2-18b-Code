import pandas as pd
import numpy as np

# Load previously saved DataFrames
df_primary = pd.read_pickle("primary_signals.pkl")
df_secondary = pd.read_pickle("secondary_signals.pkl")

# Tolerance in MHz
tolerance = 4e-6

# Extract frequency arrays
primary_freqs = df_primary['signal_frequency'].values
secondary_freqs = df_secondary['signal_frequency'].values

# Build mask: for each primary freq, check if it's NOT close to any secondary freq
mask = ~np.array([
    np.any(np.isclose(pf, secondary_freqs, atol=tolerance))
    for pf in primary_freqs
])

# Filter the primary DataFrame using the mask
primary_unique = df_primary[mask].copy()

# Save the result
primary_unique.to_pickle("primary_unique_signals.pkl")
print(f"Saved {len(primary_unique)} signals unique to Primary (not within {tolerance} MHz of Secondary) to 'primary_unique_signals.pkl'")

