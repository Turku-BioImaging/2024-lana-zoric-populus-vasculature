"""
Utility script for building Zarr group from raw data.
"""

import multiprocessing as mp
import os

import zarr
from joblib import Parallel, delayed
from skimage import io
from tqdm import tqdm
from zarr.hierarchy import Group

from .name_sanitizer import sanitize_name

RAW_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "raw_data", "Populus"
)

ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "zarr_data", "data.zarr"
)


def __process_clone_sample(clone, sample, raw_data_dir, root: Group):
    sample_path = os.path.join(raw_data_dir, clone, sample)
    raw_img = io.imread(sample_path)

    assert raw_img.ndim == 3, f"Expected 3 dimensions, got {raw_img.ndim}"
    assert raw_img.shape[2] == 3, f"Expected 3 channels, got {raw_img.shape[2]}"

    clone = sanitize_name(clone)
    sample = sanitize_name(sample)

    dataset = root.create_dataset(f"{clone}/{sample}/raw_data", data=raw_img)
    dataset.attrs.update(
        {
            "description": "Raw data",
            "clone": clone,
            "sample": sample,
            "author": "Lana Zoric, University of Novi Sad",
            "resolution": {"unit": "microns/pixel", "x": 0.0878, "y": 0.0878},
        }
    )


def convert_raw_data_to_zarr(
    raw_data_dir: str = RAW_DATA_DIR, zarr_path: str = ZARR_PATH
):
    root = zarr.open(zarr_path, mode="w")

    clone_sample_data = [
        (clone, sample)
        for clone in os.listdir(raw_data_dir)
        if os.path.isdir(os.path.join(raw_data_dir, clone))
        for sample in os.listdir(os.path.join(raw_data_dir, clone))
        if os.path.isfile(os.path.join(raw_data_dir, clone, sample))
        and (sample.endswith(".tif") or sample.endswith(".bmp"))
    ]

    assert len(clone_sample_data) > 0, "No valid samples found in raw data directory."

    Parallel(n_jobs=(mp.cpu_count()) // 2)(
        delayed(__process_clone_sample)(clone, sample, raw_data_dir, root)
        for clone, sample in tqdm(clone_sample_data)
    )


if __name__ == "__main__":
    convert_raw_data_to_zarr()
