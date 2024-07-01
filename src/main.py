"""
Main entrypoint script for image processing and analysis. Expected input is the directory containing the various Populus clones in their own folders. Directory names and file names are sanitized in the output.

Turku BioImaging, 2024
"""

import argparse
import os

from util.zarr_converter import convert_raw_data_to_zarr
from stardist_prediction.predict import StarDistPredictor

RAW_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw_data", "Populus"
)

ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "zarr_data", "data.zarr"
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--raw-data-dir",
    type=str,
    default=RAW_DATA_DIR,
    help="Path to the raw data containing directories of Populus clones.",
)

parser.add_argument(
    "--zarr-path", type=str, default=ZARR_PATH, help="Path to save Zarr data."
)

parser.add_argument(
    "--skip-raw-data", action="store_true", help="Skip copying raw data"
)

parser.add_argument(
    "--skip-stardist", action="store_true", help="Skip StarDist prediction"
)

args = parser.parse_args()

if not args.skip_raw_data:
    convert_raw_data_to_zarr(args.raw_data_dir, args.zarr_path)

if not args.skip_stardist:
    predictor = StarDistPredictor(zarr_path=args.zarr_path)
    predictor.predict_all()
