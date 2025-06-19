import pandas as pd

df=pd.read_pickle("k218b-cband-unique-dt-2.pkl")

# Step 1: Ensure 'date' column is datetime.date type
#df['date'] = pd.to_datetime(df['date']).dt.date

# Step 2: Define dates
date_08 = pd.to_datetime('2023-12-08').date()
date_14 = pd.to_datetime('2023-12-14').date()
date_19 = pd.to_datetime('2023-12-19').date()

# Step 3: Filter by each date
df_08 = df[df['date'] == date_08]
df_14 = df[df['date'] == date_14]
df_19 = df[df['date'] == date_19]

# Step 4: Combine signals from 08 and 14
combined = pd.concat([df_08, df_14])

# Step 5: Build sets of frequencies
freq_08_14 = set(combined['signal_frequency'])
freq_19 = set(df_19['signal_frequency'])

# Step 6: Find frequencies present on 08 or 14 but not on 19
exclusive_freqs = freq_08_14 - freq_19

# Step 7: Filter the combined dataframe to keep only exclusive frequencies
result = combined[combined['signal_frequency'].isin(exclusive_freqs)]

result.to_pickle("signals_dec08_14_not_19.pkl")
