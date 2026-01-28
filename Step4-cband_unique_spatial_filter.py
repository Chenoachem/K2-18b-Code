import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm  # ✅ Import tqdm

df_k218b=pd.read_pickle("k218b_cband_realdrift_realsnr.pkl")
df_other=pd.read_pickle("Other_cband_realdrift_realsnr.pkl")

# Define tolerances
freq_tol = 4e-5
drift_tol = 0.5

# Extract relevant columns as NumPy arrays
freq_other = df_other['signal_frequency'].values
drift_other = df_other['signal_drift_rate'].values

# Prepare output
matched_indices = []

# Process cband_k218b in chunks
batch_size = 500  # adjust based on available RAM
total = len(df_k218b)

for start in tqdm(range(0, total, batch_size), desc="Processing Batches"):
#for start in range(0, len(df_k218b), batch_size):
    end = min(start + batch_size, len(df_k218b))
    batch = df_k218b.iloc[start:end]
    
    freq_batch = batch['signal_frequency'].values
    drift_batch = batch['signal_drift_rate'].values

    # Broadcasting within batch
    freq_diff = np.abs(freq_batch[:, None] - freq_other[None, :]) <= freq_tol
    drift_diff = np.abs(drift_batch[:, None] - drift_other[None, :]) <= drift_tol

#    # Find rows with NO match in other
    no_match = ~np.any(freq_diff & drift_diff, axis=1)

#    # Collect indices
    matched_indices.extend(batch.index[no_match])

# Final filtered DataFrame
df_unique_rows = df_k218b.loc[matched_indices].reset_index(drop=True)

print(len(df_unique_rows))

#Write out a new pickle file with this filtered data.
df_unique_rows.to_pickle("k218b_unique_signals_c-band.pkl") #write out a new pickle file

