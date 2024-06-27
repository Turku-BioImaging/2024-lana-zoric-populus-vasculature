import os
from glob import glob
from typing import Dict, List
from skimage import io
from skimage.measure import label
from tqdm import tqdm
from skimage.segmentation import clear_border
import numpy as np
import pandas as pd
from skimage.metrics import adapted_rand_error as calculate_iou

# First perform remove objects touching boundaries and create labelled images so # that these are compatible with the predicted images


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


def process_sample(PREDICTION_DIR: str, clone: str, sample: str) -> List[Dict]:
    mask = io.imread(os.path.join(PREDICTION_DIR, clone, sample, "stardist_label.tif"))
    assert mask.ndim == 2

    mask = mask > 0

    labeled_mask = label(mask)
    

clone_data = [
    (clone, sample)
    for clone in os.listdir(PREDICTION_DIR)
    if os.path.isdir(os.path.join(PREDICTION_DIR, clone))
    for sample in os.listdir(os.path.join(PREDICTION_DIR, clone))
    if os.path.isdir(os.path.join(PREDICTION_DIR, clone, sample))
]

def calculate_iou(predicted, annotated):
    """Calculate the Intersection over Union (IoU) for a pair of images."""
    intersection = np.logical_and(predicted, annotated)
    union = np.logical_or(predicted, annotated)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def main(predicted_folder, annotated_folder, output_csv):
    iou_scores = []
    predicted_images = sorted(os.listdir(predicted_folder))
    annotated_images = sorted(os.listdir(annotated_folder))

    for pred_img, ann_img in zip(predicted_images, annotated_images):
        pred_path = os.path.join(predicted_folder, pred_img)
        ann_path = os.path.join(annotated_folder, ann_img)

        predicted = io.imread(pred_path)
        annotated = io.imread(ann_path)

        iou = calculate_iou(predicted, annotated)
        iou_scores.append((pred_img, iou))

    # Save IoU scores to a CSV file
    iou_df = pd.DataFrame(iou_scores, columns=['Image', 'IoU'])
    iou_df.to_csv(output_csv, index=False)
    print(f"IoU scores saved to {output_csv}")

if __name__ == "__main__":
    predicted_folder = os.path.join(PREDICTION_DIR)
    annotated_folder = os.path.join(OUTPUT_DIR)
    output_csv = "iou_scores.csv"
    main(predicted_folder, annotated_folder, output_csv)



