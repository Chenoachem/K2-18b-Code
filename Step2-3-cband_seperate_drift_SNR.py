import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df=pd.read_pickle("cband_cleaned.pkl")

#Going back to the original full dataframe, I a separating out the data by frequency.
cband_all = df[(df['signal_frequency'] >= 4100) & (df['signal_frequency'] <= 7900)]

#After looking at the source names per beam I realized that the source of interest is not in the same 
#beam id for each observation. So we need to filter based on name.

cband_k218b = cband_all[
    (cband_all["source_name"] == "K2-18b") |
    (cband_all["source_name"] == "3910747531814692736")
]

#Check the code
print(cband_k218b.source_name.unique())

cband_other = cband_all[
    (cband_all["source_name"] != "K2-18b") &
    (cband_all["source_name"] != "3910747531814692736") &
    (cband_all["source_name"] != "Incoherent")
]

#Check the code
print(cband_other.source_name.unique())

#Acording to the work by Meghan Li, we want to use a limit of +/- 1.9Hz/s drift rate for c-band.
cband_k218b_realdrift = cband_k218b[
    (
        (cband_k218b['signal_drift_rate'] > 0) &
        (cband_k218b['signal_drift_rate'] <= 1.9)
    ) |
    (
        (cband_k218b['signal_drift_rate'] < 0) &
        (cband_k218b['signal_drift_rate'] >= -1.9)
    )
]

#Acording to the work by Meghan Li, we want to use a limit of +/- 1.9Hz/s drift rate for c-band.
cband_other_realdrift = cband_other[
    (
        (cband_other['signal_drift_rate'] > 0) &
        (cband_other['signal_drift_rate'] <= 1.9)
    ) |
    (
        (cband_other['signal_drift_rate'] < 0) &
        (cband_other['signal_drift_rate'] >= -1.9)
    )
]


#We found with COSMIC, the false positive rate at 8sigma is high so we used 10 sigma. We also find the bright signals
#to be telescope artifacts. So we have chosen to limit between 10-100sigma.
cband_k218b_realdrift_realSNR = cband_k218b_realdrift[
    (cband_k218b_realdrift["signal_snr"] >= 10) &
    (cband_k218b_realdrift["signal_snr"] <= 100)
]
print(len(cband_k218b_realdrift_realSNR))

#We found with COSMIC, the false positive rate at 8sigma is high so we used 10 sigma. We also find the bright signals
#to be telescope artifacts. So we have chosen to limit between 10-100sigma.
cband_other_realdrift_realSNR = cband_other_realdrift[
    (cband_other_realdrift["signal_snr"] >= 10) &
    (cband_other_realdrift["signal_snr"] <= 100)
]
print(len(cband_other_realdrift_realSNR))


# Define tolerances
#freq_tol = 3e-5
#drift_tol = 0.0001

# Extract relevant columns as NumPy arrays
#freq_other = cband_other_realdrift_realSNR['signal_frequency'].values
#drift_other = cband_other_realdrift_realSNR['signal_drift_rate'].values

# Prepare output
#matched_indices = []

# Process cband_k218b in chunks
#batch_size = 1000  # adjust based on available RAM

#for start in range(0, len(cband_k218b_realdrift_realSNR), batch_size):
#    end = min(start + batch_size, len(cband_k218b_realdrift_realSNR))
#    batch = cband_k218b_realdrift_realSNR.iloc[start:end]
    
#    freq_batch = batch['signal_frequency'].values
#    drift_batch = batch['signal_drift_rate'].values

#    # Broadcasting within batch
#    freq_diff = np.abs(freq_batch[:, None] - freq_other[None, :]) <= freq_tol
#    drift_diff = np.abs(drift_batch[:, None] - drift_other[None, :]) <= drift_tol

#    # Find rows with NO match in other
#    no_match = ~np.any(freq_diff & drift_diff, axis=1)

#    # Collect indices
#    matched_indices.extend(batch.index[no_match])

# Final filtered DataFrame
#df_unique_rows = cband_k218b_realdrift_realSNR.loc[matched_indices].reset_index(drop=True)

#print(len(df_unique_rows))

#Write out a new pickle file with this filtered data.
cband_k218b_realdrift_realSNR.to_pickle("k218b_cband_realdrift_realsnr.pkl") #write out a new pickle file
cband_other_realdrift_realSNR.to_pickle("Other_cband_realdrift_realsnr.pkl")
