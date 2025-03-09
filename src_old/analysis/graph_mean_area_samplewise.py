
"""
This script calculate and plot bar graphs of mean area in micron for samples within each clone
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

# Calculate the mean area for each sample within each clone
mean_area_by_sample_clone = df.groupby(['clone', 'sample'])['area_micron'].mean().reset_index()

# Print the results
print(mean_area_by_sample_clone)

# Plot settings
sns.set(style="whitegrid")

# Get the list of unique clones
unique_clones = mean_area_by_sample_clone['clone'].unique()

# Create a bar plot for each clone
for clone in unique_clones:
    clone_data = mean_area_by_sample_clone[mean_area_by_sample_clone['clone'] == clone]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='sample', y='area_micron', hue='sample', data=clone_data, palette="viridis", dodge=False, legend=False)
    plt.title(f'Mean Area for Samples in Clone {clone}')
    plt.xlabel('Sample')
    plt.ylabel('Mean Area (micron^2)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG file
    plot_path = os.path.join(DATA_DIR, f"mean_area_by_sample_clone_{clone}.png")
    plt.savefig(plot_path)
    
