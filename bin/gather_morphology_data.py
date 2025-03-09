"""
Parses all the clone-sample combinations, generates a dataframe containing the morphological measurements of each object in the labeled images, and writes the dataframe to a CSV file.
"""

import argparse
from typing import Dict, List

import polars as pl
from dask import compute, delayed
from skimage import io
from skimage.measure import regionprops
from skimage.segmentation import relabel_sequential

PIXEL_SIZE = 0.0878  # microns (estimated from scale bars)


@delayed
def _measure_labels(clone: str, sample: str, label_path: str) -> List[Dict]:
    label_img = io.imread(label_path)
    label_img, _, _ = relabel_sequential(label_img)

    data = []

    for region in regionprops(label_img):
        data.append(
            {
                "clone": clone,
                "sample": sample,
                "label": region.label,
                "area_pixel": region.area,
                "area_micron": region.area * PIXEL_SIZE**2,
                "perimeter_pixel": region.perimeter,
                "perimeter_micron": region.perimeter * PIXEL_SIZE,
                "equivalent_diameter": region.equivalent_diameter,
                "major_axis_length": region.major_axis_length,
                "minor_axis_length": region.minor_axis_length,
                "solidity": region.solidity,
            }
        )

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)

    args = parser.parse_args()

    stream = args.data
    stream = stream.strip("[]").strip("").replace(" ", "")
    items = stream.split(",")
    clone_sample_data = [
        (items[i], items[i + 1], items[i + 2]) for i in range(0, len(items), 3)
    ]
    delayed_results = [
        _measure_labels(clone, sample, label_path)
        for clone, sample, label_path in clone_sample_data
    ]

    results = compute(*delayed_results)

    results = [item for sublist in results for item in sublist]
    df = pl.DataFrame(results)

    df.write_csv("morphology-data.csv")
