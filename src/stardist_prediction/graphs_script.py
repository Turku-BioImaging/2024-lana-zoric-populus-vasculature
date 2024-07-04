import os

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.formula.api import ols
import statsmodels.api as sm

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")

# Load the CSV file
csv_file = os.path.join(DATA_DIR, "morphology_data.csv")
# df = pl.read_csv(csv_file)
df = pl.read_csv(csv_file).to_pandas()  # Convert polars DataFrame to pandas DataFrame because 

# Plot settings
sns.set(style="whitegrid")

# Plot areas in microns
plt.figure(figsize=(15, 10))
sns.boxplot(x="clone", y="area_micron", data=df)
plt.title("Distribution of Object Areas Across Clones")
plt.xlabel("Clone")
plt.ylabel("Area (micron^2)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(DATA_DIR, "area_distribution.png"))
# plt.show()

# Perform ANOVA
model = ols('area_micron ~ C(clone)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# save the ANOVA table to a file
# anova_table.to_csv(os.path.join(DATA_DIR, "anova_results.csv"))

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
