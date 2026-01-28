import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# Load signal data (for histogram)
df = pd.read_pickle("cband_all.pkl")

# Load interval data (to shade)
intervals = pd.read_csv("Known_c-band_RFI.csv")
print("CSV columns:", intervals.columns.tolist())
# Start the plot
plt.figure(figsize=(12, 6))


# Plot histogram
sns.histplot(
    data=df,
    x="signal_frequency",
    element="step",
    stat="density",
    common_norm=False
)

# Add shaded regions and text labels
#for _, row in intervals.iterrows():
#    # Draw the shaded band
#    plt.axvspan(row['start_frequency'], row['end_frequency'], color='gray', alpha=0.3)

#    # Add the label at the center of the span
#    center_x = (row['start_frequency'] + row['end_frequency']) / 2
#    plt.text(
#        center_x,
#        plt.ylim()[1] * 0.95,  # near top of plot
#        row['label'],
#        ha='center',
#        va='top',
#        fontsize=10,
#        color='black',
#        alpha=0.8,
#        rotation=90  # optional: vertical text
#    )

# Add shaded regions (NO text labels)
first = True
for _, row in intervals.iterrows():
    plt.axvspan(
        row['start_frequency'],
        row['end_frequency'],
        color='gray',
        alpha=0.3,
        label='Known RFI' if first else None
    )
    first = False

# Add legend entry for shaded regions
shaded_patch = Patch(facecolor='gray', alpha=0.3, label='Known RFI')
handles, labels = plt.gca().get_legend_handles_labels()



# Add legend patch manually for shaded regions
#shaded_patch = Patch(facecolor='gray', alpha=0.3, label='RFI')
#plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + [shaded_patch])
# Avoid duplicate legend entries
if 'Known RFI' not in labels:
    handles.append(shaded_patch)
    labels.append('Known RFI')

plt.legend(handles=handles, labels=labels, loc='upper left')


# Final touches
plt.xlabel("Signal Frequency (MHz)",fontsize=18)
plt.ylabel("Density", fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#plt.xlim(5800,7500)
#plt.title("Signal Frequency Histogram with Shaded & Labeled Intervals")
plt.tight_layout()
#plt.show()
plt.savefig("cband_rfi_before.png",bbox_inches="tight")




