""" 
This script compares the performance of the StarDist model versus the manually annnotated shapes. Expected input data is the raw data, and the manually annotated shape files.
"""

import os
from glob import glob
from typing import Dict, List
from skimage import io
from skimage.measure import label
from tqdm import tqdm
from skimage.segmentation import clear_border
import numpy as np
import pandas as pd

# First perform remove objects touching boundaries and create labelled images so # that these are compatible with the predicted images

CLONE_SAMPLE_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "outputs"
)

# Path to annotated images directory
ANNOTATED_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stardist_data",
    "stardist_accuracy",
    "manually_annotated",
)

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stardist_data",
    "stardist_accuracy",
    "labelled_annotated",
)

annotated_img_paths = sorted(glob(os.path.join(ANNOTATED_DIR, "*.tif")))

# Loop over each annotated image path
for img_path in tqdm(annotated_img_paths):
    # Read the image
    img = io.imread(img_path)

    # Remove objects touching the border
    annotated_img = clear_border(img)

    # Apply connected component labeling
    annotated_labeled = label(annotated_img)

    # Construct the output file name
    label_fname = os.path.basename(img_path)

    # Save the labeled image
    io.imsave(
        os.path.join(OUTPUT_DIR, label_fname),
        annotated_labeled,
        check_contrast=False,
    )

# Path to predicted images directory
PREDICTION_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")


clone_data = [
    (clone, sample)
    for clone in os.listdir(PREDICTION_DIR)
    if os.path.isdir(os.path.join(PREDICTION_DIR, clone))
    for sample in os.listdir(os.path.join(PREDICTION_DIR, clone))
    if os.path.isdir(os.path.join(PREDICTION_DIR, clone, sample))
]


def calculate_iou(predicted, annotated):
    """Calculate the Intersection over Union (IoU) for a pair of images."""

    predicted = predicted > 0
    annotated = annotated > 0

    intersection = np.logical_and(predicted, annotated)
    union = np.logical_or(predicted, annotated)
    iou = np.sum(intersection) / np.sum(union)
    return iou


clone_sample_data = [
    (clone, sample)
    for clone in os.listdir(CLONE_SAMPLE_DIR)
    if os.path.isdir(os.path.join(CLONE_SAMPLE_DIR, clone))
    for sample in os.listdir(os.path.join(CLONE_SAMPLE_DIR, clone))
    if os.path.isdir(os.path.join(CLONE_SAMPLE_DIR, clone, sample))
]


def _get_prediction_fpath(annotated_img_path: str) -> str:
    clone_sample_dir_name = (
        os.path.basename(annotated_img_path)
        .replace("-", "_")
        .replace(" ", "_")
        .replace(".tif", "")
    )

    clone: str = ""
    sample: str = ""
    for clone, sample in clone_sample_data:
        if clone_sample_dir_name in sample:
            clone = clone
            sample = sample
            break

    stardist_label_path: str = os.path.join(
        CLONE_SAMPLE_DIR, clone, sample, "stardist_label.tif"
    )

    return stardist_label_path, clone_sample_dir_name


def main():
    iou_scores = []
    csv_path = "iou_scores.csv"
    annotated_img_paths = sorted(glob(os.path.join(ANNOTATED_DIR, "*.tif")))

    for annotated_img_fname in tqdm(annotated_img_paths):
        stardist_label_path, prediction_img_name = _get_prediction_fpath(annotated_img_fname)
        annotated_img_name = os.path.basename(annotated_img_fname)
        annotated_img_path = os.path.join(OUTPUT_DIR, annotated_img_name)

        pred_img = io.imread(stardist_label_path)
        gt_img = io.imread(annotated_img_path)

        iou = calculate_iou(pred_img, gt_img)
        # iou_scores.append(iou)
        iou_scores.append((prediction_img_name, annotated_img_name, iou))

    # Save IoU scores to a CSV file
    # iou_df = pd.DataFrame(iou_scores, columns=["Image", "IoU"])
    iou_df = pd.DataFrame(iou_scores, columns=["Prediction Image", "Ground Truth Image", "IoU"])
    iou_df.to_csv(csv_path, index=False)
    print(f"IoU scores saved to {csv_path}")


if __name__ == "__main__":
    main()
