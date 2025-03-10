"""
This script generates labeled images from shapefiles and raw images.

Usage:
    python generate_labels_from_shapes.py --image-path <path_to_image> --shapefile-path <path_to_shapefile>

Arguments:
    --image-path: Path to the raw image file.
    --shapefile-path: Path to the shapefile in CSV format.

The script reads a shapefile and a raw image, processes the shapefile to extract polygon shapes, 
and generates a labeled image where each polygon is assigned a unique label. The labeled image 
is saved as "labels.tif", and the raw image and shapefile are copied to "raw-image.tif" and "shapes.csv" respectively.

"""
import argparse
import shutil
import numpy as np
import polars as pl
from rasterio.features import rasterize
from shapely.geometry import Polygon
from skimage import io
from skimage.measure import label
from skimage.segmentation import clear_border


def _shapefile_to_label_img(shapefile_path: str, raw_img_path: str) -> np.ndarray:
    raw_img = io.imread(raw_img_path)
    assert raw_img.ndim == 3
    assert raw_img.shape[-1] == 3
    assert raw_img.dtype == np.uint8

    df = pl.read_csv(shapefile_path)

    df = (
        df.select(["index", "shape-type", "axis-0", "axis-1"])
        .filter(pl.col("shape-type") == "polygon")
        .rename({"axis-0": "y", "axis-1": "x"})
    )

    df = df.with_columns(
        df["y"].map_elements(round, return_dtype=pl.Int32).alias("y"),
        df["x"].map_elements(round, return_dtype=pl.Int32).alias("x"),
    ).group_by(["index"])

    complete_mask = np.zeros(raw_img.shape[:2], dtype=bool)

    for _, polygon_data in df:
        polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
        polygon_mask = rasterize([polygon], out_shape=raw_img.shape[:2])
        complete_mask[polygon_mask == 1] = 1

    complete_mask = label(complete_mask)
    complete_mask = clear_border(complete_mask)

    return complete_mask


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-path", type=str, required=True)
    parser.add_argument("--shapefile-path", type=str, required=True)
    args = parser.parse_args()

    # Make raster labels
    label_img = _shapefile_to_label_img(args.shapefile_path, args.image_path)
    io.imsave("labels.tif", label_img.astype(np.uint32), check_contrast=False)

    shutil.copy(args.image_path, "raw-image.tif")
    shutil.copy(args.shapefile_path, "shapes.csv")

