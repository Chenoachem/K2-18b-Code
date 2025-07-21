import pandas as pd
import numpy as np

# Load your data
df = pd.read_pickle("primary_unique_signals.pkl")  # change filename as needed

# Ensure date column is datetime.date
df['date'] = pd.to_datetime(df['date']).dt.date

#    2023-10-13
#    2023-10-22
#    2023-12-21


# Define your date objects
date_13 = pd.to_datetime('2023-10-13').date()
date_21 = pd.to_datetime('2023-12-21').date()
date_22 = pd.to_datetime('2023-10-22').date()

# Filter the DataFrame to get data for each date
df_13 = df[df['date'] == date_13]
df_21 = df[df['date'] == date_21]
df_22 = df[df['date'] == date_22]

# Now extract signal frequencies
freq_13 = df_13['signal_frequency'].values
freq_21 = df_21['signal_frequency'].values
freq_22 = df_22['signal_frequency'].values

# Define tolerance (in MHz)
freq_tol = 4e-6  # 4 Hz = 4e-6 MHz

# Find unique-to-Dec-13 frequencies
mask_13 = ~np.array([
    np.any(np.isclose(f, freq_21, atol=freq_tol)) or np.any(np.isclose(f, freq_22, atol=freq_tol))
    for f in freq_13
])
unique_13 = df_13.iloc[mask_13]

# Find unique-to-Dec-21 frequencies
mask_21 = ~np.array([
    np.any(np.isclose(f, freq_13, atol=freq_tol)) or np.any(np.isclose(f, freq_22, atol=freq_tol))
    for f in freq_21
])
unique_21 = df_21.iloc[mask_21]

# Find unique-to-Dec-22 frequencies
mask_22 = ~np.array([
    np.any(np.isclose(f, freq_13, atol=freq_tol)) or np.any(np.isclose(f, freq_21, atol=freq_tol))
    for f in freq_22
])
unique_22 = df_22.iloc[mask_22]

# Combine results
df_unique_all = pd.concat([unique_13, unique_21, unique_22]).reset_index(drop=True)

# Save result
df_unique_all.to_pickle("unique_signals_13_21_22.pkl")
print(f"Saved {len(df_unique_all)} unique signals from Dec 13, 21, and 22 to 'unique_signals_13_21_22.pkl'")
