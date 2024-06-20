import os

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")

# Load the CSV file
csv_file = os.path.join(DATA_DIR, "object_sizes.csv")
df = pl.read_csv(csv_file)

# Convert to pandas DataFrame for easier plotting with seaborn/matplotlib
df = df.to_pandas()

# Plot settings
sns.set(style="whitegrid")

# Plot areas in microns
plt.figure(figsize=(15, 10))
sns.boxplot(x='clone', y='area_micron', data=df)
plt.title('Distribution of Object Areas Across Clones')
plt.xlabel('Clone')
plt.ylabel('Area (micron^2)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "area_distribution.png"))
plt.show()

# Plot perimeters in microns
plt.figure(figsize=(15, 10))
sns.boxplot(x='clone', y='perimeter_micron', data=df)
plt.title('Distribution of Object Perimeters Across Clones')
plt.xlabel('Clone')
plt.ylabel('Perimeter (microns)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "perimeter_distribution.png"))
plt.show()
