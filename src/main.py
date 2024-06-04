"""
Main entrypoint script for image processing and analysis. Expected input is the directory containing the various Populus clones in their own folders. Directory names and file names are sanitized in the output.

Turku BioImaging, 2024
"""

import argparse
import os
from glob import glob

from raw_data import copy_raw_data_to_output
from tqdm import tqdm

RAW_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw_data", "Populus"
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "outputs")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--raw-data-dir",
    type=str,
    default=RAW_DATA_DIR,
    help="Path to the raw data containing directories of Populus clones.",
)
parser.add_argument(
    "--output-dir", type=str, default=OUTPUT_DIR, help="Path to save outputs."
)
parser.add_argument(
    "--skip-raw-data", action="store_true", help="Skip copying raw data"
)
parser.add_argument(
    "--overwrite", type=bool, default=True, help="Overwrite existing images."
)

args = parser.parse_args()


clone_dirs = [
    items
    for items in os.listdir(RAW_DATA_DIR)
    if os.path.isdir(os.path.join(RAW_DATA_DIR, items))
]

for clone_dir in clone_dirs:
    sample_names = [
        os.path.basename(sample_name)
        for sample_name in glob(os.path.join(RAW_DATA_DIR, clone_dir, "*.tif"))
    ]

    for sample_name in tqdm(sample_names, desc=f"Copying {clone_dir} samples..."):
        copy_raw_data_to_output(
            raw_data_dir=args.raw_data_dir,
            output_dir=args.output_dir,
            clone_name=clone_dir,
            sample_name=sample_name,
        )
