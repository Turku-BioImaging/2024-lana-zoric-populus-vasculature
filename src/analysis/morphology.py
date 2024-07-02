import os
from glob import glob
from typing import Any, Dict, List

import numpy as np
import polars as pl
import zarr
from skimage.measure import regionprops
from tqdm import tqdm
from util.shapefile import shapefile_to_label_img

from src.util.name_sanitizer import find_matching_shapefile

ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "zarr_data", "data.zarr"
)

SHAPE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stardist_data",
    "images_for_annotation",
    "shapes",
)

PIXEL_SIZE = 0.0878


def __measure_labels(label_img: np.ndarray) -> List[Dict]:
    data = []

    for region in regionprops(label_img):
        data.append(
            {
                "label": region.label,
                "area_pixel": region.area,
                "area_micron": region.area * PIXEL_SIZE**2,
                "perimeter_pixel": region.perimeter,
                "perimeter_micron": region.perimeter * PIXEL_SIZE,
                # "centroid": region.centroid,
                # "convex_area": region.convex_area,
                # "eccentricity": region.eccentricity,
                "equivalent_diameter": region.equivalent_diameter,
                "major_axis_length": region.major_axis_length,
                "minor_axis_length": region.minor_axis_length,
                "solidity": region.solidity,
            }
        )

    return data


def process_zarr_data(zarr_path: str):
    root = zarr.open_group(zarr_path, mode="r")

    clone_sample_data = [
        (clone, sample)
        for clone in list(root.keys())
        for sample in list(root[clone].keys())
    ]

    shapefile_paths = glob(os.path.join(SHAPE_DIR, "*.csv"))

    clone_data = []

    for clone, sample in tqdm(clone_sample_data):
        shapefile_path = find_matching_shapefile(
            shape_paths=shapefile_paths, sample=sample
        )
        assert shapefile_path is not None, f"No matching shapefile found for {sample}"

        raw_data: Any = root[f"{clone}/{sample}/raw_data"][:]

        label_img: np.ndarray = shapefile_to_label_img(
            shapefile_path, raw_data.shape[:-1]
        )

        sample_data = []
        for region_data in __measure_labels(label_img):
            sample_data.append({"clone": clone, "sample": sample, **region_data})

        clone_data.extend(sample_data)

    clone_data_df = pl.DataFrame(clone_data)
    clone_data_df.write_csv("morphology_data.csv")


def main():
    process_zarr_data(ZARR_PATH)


if __name__ == "__main__":
    main()
