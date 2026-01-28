import pandas as pd
import numpy as np

# Load your signal data (from .pkl)
df = pd.read_pickle("cband_all.pkl")


# Load and clean RFI CSV
rfi_ranges = pd.read_csv("Known_c-band_RFI.csv", header=None).iloc[:, :2]
rfi_ranges.columns = ['start_frequency', 'end_frequency']
#coerce means to convert to int if a number and make a NaN if not.
rfi_ranges['start_frequency'] = pd.to_numeric(rfi_ranges['start_frequency'], errors='coerce')
rfi_ranges['end_frequency'] = pd.to_numeric(rfi_ranges['end_frequency'], errors='coerce')
rfi_ranges = rfi_ranges.dropna(subset=['start_frequency', 'end_frequency'])

# Define a mask to filter out RFI-contaminated signals
def is_rfi(frequency, ranges):
    # Check if frequency is inside any RFI range
    return np.any((frequency >= ranges['start_frequency']) & (frequency <= ranges['end_frequency']))

# Apply the filter across the DataFrame
mask = df['signal_frequency'].apply(lambda f: not is_rfi(f, rfi_ranges))

# Filtered DataFrame: signals outside known RFI ranges
df_clean = df[mask].reset_index(drop=True)
print(len(df['signal_frequency']))

# Save to new pickle file
df_clean.to_pickle("cband_cleaned.pkl")

#cband_k218b_realdrift_realSNR = df_clean[
#	(df_clean["signal_snr"] >= 15) &
#	(df_clean["signal_snr"] <= 100)
#	]
#print(len(df_clean)


# Optional: Feedback
#print(f"Original: {len(df)} rows")
#print(f"Filtered: {len(df_clean)} rows")
#print(f"Saved cleaned result to 'unique_signals_08_14_nozerodrift_cleaned_R2.pkl'")

