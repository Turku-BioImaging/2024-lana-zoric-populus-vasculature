"""
Measure the accuracy of StarDist predictions against the ground truth. Reads data from the Zarr group and manual shape files. Shape files are no longer saved to TIFF label images, instead they care converted to numpy arrays during execution.
"""

import os
from glob import glob
from typing import Any

import numpy as np
import polars as pl
import zarr
from joblib import Parallel, delayed
from rasterio.features import rasterize
from shapely.geometry import Polygon
from skimage.measure import label
from skimage.segmentation import clear_border
from tqdm import tqdm
from zarr.hierarchy import Group

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


def __calculate_iou(predicted, annotated):
    predicted = predicted > 0
    annotated = annotated > 0

    intersection = np.logical_and(predicted, annotated)
    union = np.logical_or(predicted, annotated)
    iou = np.sum(intersection) / np.sum(union)
    return iou


# def __calculate_iou_per_label(predicted, annotated, label_id) -> float:
#     pred_label = predicted == label_id
#     anno_label = annotated == label_id

#     intersection = np.logical_and(pred_label, anno_label)
#     union = np.logical_or(pred_label, anno_label)
#     if np.sum(union) == 0:
#         return 0.0
#     iou = np.sum(intersection) / np.sum(union)
#     return iou



def __shapefile_to_label_img(
    shapefile_path, clone: str, sample: str, root: Group
) -> np.ndarray:
    raw_data = root[f"{clone}/{sample}/raw_data"][:]

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

    complete_mask: Any = np.zeros(raw_data.shape[:-1], dtype=bool)  # type: ignore

    for _, polygon_data in df:
        polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
        polygon_mask = rasterize([polygon], out_shape=raw_data.shape[:-1])
        complete_mask[polygon_mask == 1] = 1

    complete_mask = clear_border(complete_mask)
    complete_mask = label(complete_mask)
    return complete_mask


def __process_sample(root: Group, shape_paths: list, clone: str, sample: str):
    shapefile_path = find_matching_shapefile(shape_paths, sample)

    gt_labels = __shapefile_to_label_img(
        shapefile_path=shapefile_path, clone=clone, sample=sample, root=root
    )

    pred_labels = root[f"{clone}/{sample}/stardist_labels"][:]

    assert (
        gt_labels.shape == pred_labels.shape
    ), "Ground truth and prediction label dimensions do not match."

    iou = __calculate_iou(predicted=pred_labels, annotated=gt_labels)

    data = {"clone": clone, "sample": sample, "iou": iou}
    return data
    
    # gt_unique_labels = np.unique(gt_labels)
    # pred_unique_labels = np.unique(pred_labels)

    # results = []
    # for label_id in np.union1d(gt_unique_labels, pred_unique_labels):
    #     iou = __calculate_iou_per_label(predicted=pred_labels, annotated=gt_labels, label_id=label_id)
    #     results.append({"clone": clone, "sample": sample, "label_id": label_id, "iou": iou})

    # return results

def main():
    root = zarr.open_group(ZARR_PATH, mode="a")
    SHAPE_PATHS = glob(os.path.join(SHAPE_DIR, "*.csv"))

    clone_sample_data = [
        (clone, sample)
        for clone in list(root.keys())
        for sample in list(root[clone].keys())
    ]

    data = Parallel(n_jobs=-1)(
        delayed(__process_sample)(root, SHAPE_PATHS, clone, sample)
        for clone, sample in tqdm(clone_sample_data)
    )

    df = pl.DataFrame(data)
    df.write_csv(os.path.join(os.path.dirname(__file__), "iou_scores.csv"))

    # flat_data = [item for sublist in all_data for item in sublist]
    # df = pl.DataFrame(flat_data)
    # df.write_csv(os.path.join(os.path.dirname(__file__), "label_iou_scores.csv"))

if __name__ == "__main__":
    main()
