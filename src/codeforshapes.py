"""
Generates label images from vector shape files.
"""

import os
from glob import glob

import numpy as np
import polars as pl
from rasterio.features import rasterize
from shapely.geometry import Polygon
from skimage import io
from skimage.measure import label
from tqdm import tqdm

# Path to shape directory
SHAPE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "stardist_data",
    "images_for_annotation",
    "remaining_anot",
)

IMG_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "stardist_data",
    "images_for_annotation",
    "remaining_img",
)

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "stardist_data", "labelsNew"
)

shapefile_paths = sorted(glob(os.path.join(SHAPE_DIR, "*.csv")))
img_paths = sorted(glob(os.path.join(IMG_DIR, "*.tif")))

data_paths = list(zip(img_paths, shapefile_paths))

for item in tqdm(data_paths):
    img_path, shapefile_path = item

    assert (
        os.path.basename(shapefile_path).split(".")[0]
        == os.path.basename(img_path).split(".")[0]
    )

    img = io.imread(img_path)

    # Read and process the shape CSV file
    df = (
        pl.read_csv(shapefile_path)
        .select(["index", "shape-type", "axis-0", "axis-1"])
        .filter(pl.col("shape-type") == "polygon")
        .rename({"axis-0": "y", "axis-1": "x"})
    )

    # Round the coordinates and group by 'index'
    df = df.with_columns(
        df["y"].map_elements(round, return_dtype=pl.Int32).alias("y"),
        df["x"].map_elements(round, return_dtype=pl.Int32).alias("x"),
    ).group_by(["index"])

    complete_mask = np.zeros(img.shape[:-1], dtype=bool)

    for _, polygon_data in df:
        polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
        polygon_mask = rasterize([polygon], out_shape=img.shape[:-1])
        complete_mask[polygon_mask == 1] = 1

    label_fname = os.path.basename(img_path)
    label_img = label(complete_mask)
    io.imsave(
        os.path.join(OUTPUT_DIR, label_fname),
        label_img,
        check_contrast=False,
    )
