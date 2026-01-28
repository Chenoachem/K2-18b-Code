import pandas as pd

# Load the two pickle files
df_incoherent = pd.read_pickle("cband_incoherent.pkl")
df_sources = pd.read_pickle("cband_signals_unique_across_3days_tol2Hz_by_drift.pkl")

# Filter df_sources for the two source_names of interest
df_sources = df_sources[df_sources['source_name'].isin(["K2-18b", "3910747531814692736"])]

# --- STEP 1: Find exact matches ---
df_matches = pd.merge(
    df_incoherent,
    df_sources,
    on=['tstart', 'signal_frequency', 'signal_drift_rate'],
    suffixes=('_incoherent', '_source')
)

# Save the matched DataFrame
df_matches.to_pickle("matched_signals.pkl")
df_matches.to_csv("matched_signals.csv", index=False)
print(f"✅ Saved {len(df_matches)} matched signals to 'matched_signals.pkl' and 'matched_signals.csv'")

# --- STEP 2: Find coherent signals NOT in incoherent ---
df_coherent_unique = df_sources.merge(
    df_incoherent[['tstart', 'signal_frequency', 'signal_drift_rate']],
    on=['tstart', 'signal_frequency', 'signal_drift_rate'],
    how='left',
    indicator=True
)

# Keep only those that did NOT match
df_coherent_unique = df_coherent_unique[df_coherent_unique['_merge'] == 'left_only'].drop(columns=['_merge'])

# Save this unique coherent signals DataFrame
df_coherent_unique.to_pickle("coherent_not_in_incoherent_cband.pkl")
df_coherent_unique.to_csv("coherent_not_in_incoherent_cband.csv", index=False)

print(f"✅ Saved {len(df_coherent_unique)} coherent-only signals to 'coherent_not_in_incoherent.pkl' and 'coherent_not_in_incoherent.csv'")

