import matplotlib.pyplot as plt

import seaborn as sns

import pandas as pd

df=pd.read_pickle('Final_Code/K2-18b-hits_02-14-24-2.pkl')
 

from astropy.time import Time

t = Time(df["tstart"].values, format="mjd", scale="utc") 
df["utc_datetime"] = t.to_datetime()

sns.set_theme(
    context="paper",
    style="darkgrid",
    rc={
        "axes.facecolor": "#f0f0f0",   # light gray
        "grid.color": "white",
        "grid.linestyle": "-",
        "axes.labelsize": 18,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
    }
)

plt.figure(figsize=(6, 5))
   
sns.scatterplot(
    data=df,
    x="utc_datetime",
    y="signal_frequency",
    s=20
)
    
plt.xticks(rotation=45)
plt.xlabel("Date",fontsize=18)
plt.ylabel("Frequency (MHz)",fontsize=18)

    
plt.tight_layout()
#plt.show()
plt.savefig('COSMIC_Data_All_Epochs.png',bbox_inches='tight')

df["utc_minute"] = df["utc_datetime"].dt.round("T")

# Keep one row per unique minute (first occurrence)
unique_rows = df.drop_duplicates(subset="utc_minute").sort_values("utc_minute")

# Write to a text file
outfile = "unique_times_and_freqs.txt"

with open(outfile, "w") as f:
    for _, row in unique_rows.iterrows():
        time_str = row["utc_minute"].strftime("%Y-%m-%d %H:%M")
        freq = row["signal_frequency"]
        f.write(f"{time_str}  {freq}\n")

print(f"Wrote {len(unique_rows)} entries to {outfile}")


