import os

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

import scipy.stats as stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")

# Load the CSV file
csv_file = os.path.join(DATA_DIR, "morphology_data.csv")
# df = pl.read_csv(csv_file)
df = pl.read_csv(csv_file).to_pandas()  # Convert polars DataFrame to pandas DataFrame because 

# Plot settings
# sns.set(style="whitegrid")

# # Plot areas in microns (boxplot)
# plt.figure(figsize=(15, 10))
# sns.boxplot(x="clone", y="area_micron", data=df)
# plt.title("Distribution of Object Areas Across Clones")
# plt.xlabel("Clone")
# plt.ylabel("Area (micron^2)")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig(os.path.join(DATA_DIR, "area_distribution.png"))
# # plt.show()


# List of clones
clones = df['clone'].unique()

# Plot settings
sns.set(style="whitegrid")

# Create a directory to save the plots
output_dir = os.path.join(DATA_DIR, "output_graphs")
os.makedirs(output_dir, exist_ok=True)

# Iterate over each clone to check distribution
for clone in clones:
    clone_data = df[df['clone'] == clone]['area_micron']
    
    # Plot histogram and KDE
    plt.figure(figsize=(12, 6))
    sns.histplot(clone_data, kde=True)
    plt.title(f'Histogram and KDE for {clone}')
    plt.xlabel('Area (micron^2)')
    plt.ylabel('Density')
    plt.savefig(os.path.join(output_dir, f'{clone}_hist_kde.png'))
    plt.close()
    
    
    # Shapiro-Wilk Test
    shapiro_stat, shapiro_p = stats.shapiro(clone_data)
    print(f'{clone} - Shapiro-Wilk Test: Statistics={shapiro_stat}, p-value={shapiro_p}')



# Perform ANOVA test (gives difference in mean area across different clones)
model = ols('area_micron ~ C(clone)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# # # save the ANOVA table to a file
# # anova_table.to_csv(os.path.join(DATA_DIR, "anova_results.csv"))

# Calculate the mean area for each clone
mean_area_by_clone = df.groupby('clone')['area_micron'].mean().reset_index()

# Print the results
print(mean_area_by_clone)
# save the results to a CSV file
mean_area_by_clone.to_csv(os.path.join(DATA_DIR,"mean_area_by_clone.csv"))

# plot for mean area

# Load the CSV file
csv_file = os.path.join(DATA_DIR, "mean_area_by_clone.csv")
# df = pl.read_csv(csv_file)
df = pl.read_csv(csv_file).to_pandas()

# Plot settings
sns.set(style="whitegrid")

# Create a bar plot for mean area by clone
plt.figure(figsize=(12, 8))
sns.barplot(x='clone', y='area_micron', data=mean_area_by_clone, palette="viridis")
plt.title('Mean Area for Each Clone')
plt.xlabel('Clone')
plt.ylabel('Mean Area (micron^2)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "mean_area_by_clone.png"))

# # Perform Tukey's HSD test to check which clones are different 
# tukey_results = pairwise_tukeyhsd(df['area_micron'], df['clone'], alpha=0.05)

# print(tukey_results)

# # Plot Tukey's HSD results
# plt.figure(figsize=(10, 6))
# tukey_results.plot_simultaneous()
# plt.title("Tukey's HSD Test for Clone Groups")
# plt.xlabel("Mean Difference")
# plt.ylabel("Clone")
# plt.tight_layout()
# plt.savefig(os.path.join(DATA_DIR, "tukey_hsd.png"))

# # Plot distributions of area_micron for each clone (violin plots)
# plt.figure(figsize=(15, 10))
# sns.violinplot(x="clone", y="area_micron", data=df, inner="quartile")
# plt.title("Distribution of Object Areas Across Clones")
# plt.xlabel("Clone")
# plt.ylabel("Area (micron^2)")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig(os.path.join(DATA_DIR, "area_distribution_by_clone.png"))

# # Save the figure showing distributions by clone
# plt.savefig(os.path.join(DATA_DIR, "area_distribution_by_clone.png"))

# # Plot perimeters in microns
# plt.figure(figsize=(15, 10))
# sns.boxplot(x="clone", y="perimeter_micron", data=df)
# plt.title("Distribution of Object Perimeters Across Clones")
# plt.xlabel("Clone")
# plt.ylabel("Perimeter (microns)")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig(os.path.join(DATA_DIR, "perimeter_distribution.png"))
# # plt.show()
