import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Load data
df = pd.read_pickle("cband_k218b.pkl")

# Set style
sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})

# Split data by source_name
highlight = df[df['source_name'] == "K2-18b"]
others = df[df['source_name'] != "K2-18b"]

# Create figure
plt.figure(figsize=(8, 6))

# Plot other sources
sns.scatterplot(data=others, x="ra_hours", y="dec_degrees", marker='o', color='gray', label='Other Sources')

# Plot highlighted source
sns.scatterplot(data=highlight, x="ra_hours", y="dec_degrees", marker='*', color='red', label='K2-18b')

# Add main 7 arcmin circle
ra_center = 11.50
dec_center = highlight['dec_degrees'].mean() if not highlight.empty else df['dec_degrees'].mean()
radius_deg = 7 / 60  # 7 arcmin in degrees
main_circle = Circle((ra_center, dec_center), radius_deg, edgecolor='blue', facecolor='none', linewidth=1.5, label='PB FWHM')
plt.gca().add_patch(main_circle)

# Determine plot limits first
ra_min, ra_max = plt.xlim()
dec_min, dec_max = plt.ylim()

# Add small 12 arcsecond circle in the bottom right
radius_small = 6 / 3600  # 6 arcsec in degrees
padding_ra = 0.01  # horizontal padding
padding_dec = 0.01  # vertical padding

small_circle = Circle((ra_max - padding_ra, dec_min + padding_dec), radius_small,
                      edgecolor='black', facecolor='none', linewidth=1.2, label='12 arcsec diameter')
plt.gca().add_patch(small_circle)

# Maintain equal aspect ratio
plt.gca().set_aspect('equal', adjustable='box')

# Label axes
plt.xlabel("RA (hours)",fontsize=18)
plt.ylabel("Dec (degrees)",fontsize=18)
plt.tick_params(axis='both', labelsize=16)


plt.legend()

plt.savefig("Source_positions_FWHM_syth.png", bbox_inches="tight")
