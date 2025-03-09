import polars as pl
import numpy as np
import os
from skimage.measure import label
from rasterio.features import rasterize
from shapely.geometry import Polygon
from skimage.segmentation import clear_border
from typing import Any


def shapefile_to_label_img(shapefile_path, img_shape: tuple) -> np.ndarray:
    assert os.path.isfile(shapefile_path), f"File not found: {shapefile_path}"
    assert len(img_shape) == 2, f"Image shape must be 2D, got {len(img_shape)}D"

    df = (
        pl.read_csv(shapefile_path)
        .select(["index", "shape-type", "axis-0", "axis-1"])
        .filter(pl.col("shape-type") == "polygon")
        .rename({"axis-0": "y", "axis-1": "x"})
    )

    df = df.with_columns(
        df["y"].map_elements(round, return_dtype=pl.Int32).alias("y"),
        df["x"].map_elements(round, return_dtype=pl.Int32).alias("x"),
    ).group_by(["index"])

    complete_mask: Any = np.zeros(img_shape, dtype=bool)  # type: ignore

    for _, polygon_data in df:
        polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
        polygon_mask = rasterize([polygon], out_shape=img_shape)
        complete_mask[polygon_mask == 1] = 1

    complete_mask = label(complete_mask)
    complete_mask = clear_border(complete_mask)

    return complete_mask
