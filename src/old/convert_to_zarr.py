"""
Utility script to convert the raw data into a Zarr group. Additionally, file and folder names are also modified to be more readable and reliable.
"""

import os
from glob import glob

import numpy as np
import zarr
from skimage import io
from tqdm import tqdm

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "raw_data")
ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "zarr_data", "plant-vasculatur-data.zarr"
)

EXCLUSION_LIST = ["181-81 1a.tif"]

if __name__ == "__main__":

    root = zarr.open(ZARR_PATH, mode="w")

    clone_names = [
        d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))
    ]

    for clone_name in clone_names:
        clone_path = os.path.join(DATA_DIR, clone_name)
        clone_name = (
            clone_name.replace(" +", "+")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )

        c_dataset = root.create_group(clone_name)
        c_dataset.attrs["author"] = "Lana Zoric, University of Novi Sad"

        sample_paths = glob(os.path.join(clone_path, "*.tif"))

        sample_names = []

        for sample_path in tqdm(sample_paths):

            if os.path.basename(sample_path) in EXCLUSION_LIST:
                continue
            sample_name = (
                os.path.basename(sample_path)
                .replace(".tif", "")
                .replace(" ", "_")
                .replace("-", "_")
            )

            img = io.imread(sample_path)

            assert img.shape == (3000, 4000, 3)
            assert img.dtype == np.uint8

            s_group = c_dataset.create_group(sample_name)
            s_dataset = s_group.create_dataset("raw_data", data=img)
            s_dataset.attrs["description"] = "Raw data"
            s_dataset.attrs["author"] = "Lana Zoric, University of Novi Sad"
            s_dataset.attrs["resolution"] = {
                "unit": "microns/pixel",
                "x": 0.087,
                "y": 0.087,
            }
