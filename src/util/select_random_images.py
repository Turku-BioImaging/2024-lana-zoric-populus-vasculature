"""
Select random images from the raw data, to be manually labeled for use in training a StarDist model.
"""

from skimage import io
import os
from tqdm import tqdm
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stardist_data",
    "images_for_annotation",
    "images",
)

clone_data = [
    (clone, sample)
    for clone in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, clone))
    for sample in os.listdir(os.path.join(DATA_DIR, clone))
    if os.path.isdir(os.path.join(DATA_DIR, clone, sample))
]

np.random.seed(4425)
np.random.shuffle(clone_data)

clone_data = clone_data[:30]

for item in tqdm(clone_data):
    clone, sample = item
    image_path = os.path.join(DATA_DIR, clone, sample, "raw_data.tif")
    img = io.imread(image_path)
    assert img.ndim == 3, f"Expected 3 dimensions, got {img.ndim}"
    assert img.shape[2] == 3, f"Expected 3 channels, got {img.shape[2]}"

    output_path = os.path.join(OUTPUT_DIR, f"{sample}.tif")
    io.imsave(output_path, img, check_contrast=False)
