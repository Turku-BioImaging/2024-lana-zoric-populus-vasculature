"""
This code first calculate mean area in micron for each clone and then plot the bar graph for mean area for each clone  
"""

import os
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the directory and CSV file path
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")
csv_file = os.path.join(DATA_DIR, "morphology_data.csv")

# Load the CSV file
df = pl.read_csv(csv_file)

# Convert to pandas DataFrame for compatibility with groupby and plotting
df = df.to_pandas()

# Calculate the mean area for each clone
mean_area_by_clone = df.groupby('clone')['area_micron'].mean().reset_index()

# Print the results
print(mean_area_by_clone)

# Plot settings
sns.set(style="whitegrid")

# Create a bar plot for mean area by clone
plt.figure(figsize=(12, 8))
sns.barplot(x='clone', y='area_micron', hue='clone', data=mean_area_by_clone, palette="viridis", dodge=False, legend=False)
plt.title('Mean Area for Each Clone')
plt.xlabel('Clone')
plt.ylabel('Mean Area (micron^2)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as a PNG file
plot_path = os.path.join(DATA_DIR, "mean_area_by_clone.png")
plt.savefig(plot_path)


