import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# Load signal data (for histogram)
df = pd.read_pickle("unique_signals_08_14_nozerodrift_cleaned_2.pkl")

# Load interval data (to shade)
intervals = pd.read_csv("Known_c-band_RFI.csv")
print("CSV columns:", intervals.columns.tolist())
# Start the plot
plt.figure(figsize=(12, 6))


# Plot histogram
sns.histplot(
    data=df,
    x="signal_frequency",
    hue="date",
    element="step",
    stat="density",
    common_norm=False
)

# Add shaded regions and text labels
for _, row in intervals.iterrows():
    # Draw the shaded band
    plt.axvspan(row['start_frequency'], row['end_frequency'], color='gray', alpha=0.3)

    # Add the label at the center of the span
    center_x = (row['start_frequency'] + row['end_frequency']) / 2
    plt.text(
        center_x,
        plt.ylim()[1] * 0.95,  # near top of plot
        row['label'],
        ha='center',
        va='top',
        fontsize=10,
        color='black',
        alpha=0.8,
        rotation=90  # optional: vertical text
    )

# Add legend patch manually for shaded regions
#shaded_patch = Patch(facecolor='gray', alpha=0.3, label='RFI')
#plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + [shaded_patch])

# Final touches
plt.xlabel("Signal Frequency (MHz)")
plt.ylabel("Density")
#plt.xlim(5800,7500)
plt.title("Signal Frequency Histogram with Shaded & Labeled Intervals")
plt.tight_layout()
plt.show()





