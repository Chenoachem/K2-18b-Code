import pandas as pd

# Load the two pickle files
df_incoherent = pd.read_pickle("sband_incoherent.pkl")
df_sources = pd.read_pickle("sband-signals_unique_across_3days_tol2Hz_by_drift.pkl")

# Filter df_sources for the two source_names of interest
df_sources = df_sources[df_sources['source_name'].isin(["K2-18b", "3910747531814692736"])]

# Perform exact matches using an inner merge on tstart, signal_frequency, and signal_drift_rate
df_matches = pd.merge(
    df_incoherent,
    df_sources,
    on=['tstart', 'signal_frequency', 'signal_drift_rate'],
    suffixes=('_incoherent', '_source')
)

# Save the matched DataFrame
df_matches.to_pickle("matched_signals_sband_2.pkl")
df_matches.to_csv("matched_signals_sband_2.csv", index=False)

print(f"✅ Saved {len(df_matches)} matched signals to 'matched_signals.pkl' and 'matched_signals.csv'")

