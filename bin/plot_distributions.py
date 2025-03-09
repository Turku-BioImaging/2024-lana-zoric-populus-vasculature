import os
import argparse
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-csv", type=str, required=True)
    args = parser.parse_args()

    sns.set_theme(style="whitegrid")

    df = pl.read_csv(args.data_csv)
    clone_groups = df.group_by("clone")

    # Plot sample-wise clone distributions
    for clone, group in clone_groups:
        samples = group["sample"].unique()

        os.makedirs(os.path.join("plots", clone[0]), exist_ok=True)

        # Areas box plots
        plt.figure(figsize=(15, 10))
        sns.boxplot(x="sample", y="area_micron", data=group.to_pandas())
        plt.title(f"Distribution of Object Areas in Clone {clone[0]}")
        plt.xlabel("Sample")
        plt.ylabel("Area (micron^2)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join("plots", clone[0], "area_distribution.png"))

        # Perimeters box plots
        plt.figure(figsize=(15, 10))
        sns.boxplot(x="sample", y="perimeter_micron", data=group.to_pandas())
        plt.title(f"Distribution of Object Perimeters in Clone {clone[0]}")
        plt.xlabel("Sample")
        plt.ylabel("Perimeter (microns)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join("plots", clone[0], "perimeter_distribution.png"))

    # Plot clone distributions
    plt.figure(figsize=(15, 10))
    sns.violinplot(x="clone", y="area_micron", data=df.to_pandas(), hue="clone")
    plt.title("Distribution of Object Areas per Clone")
    plt.xlabel("Clone")
    plt.ylabel("Area (micron^2)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "area_distribution_per_clone.png"))
