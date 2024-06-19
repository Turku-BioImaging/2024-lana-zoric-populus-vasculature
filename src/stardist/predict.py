"""
Experimental StarDist prediction script for custom data.
"""

import os
from tqdm import tqdm
import numpy as np
from skimage import io
from csbdeep.utils import normalize
from stardist.models import StarDist2D
from skimage.transform import rescale


def downscale_image(img_path: str, scale_factor: float = 0.10) -> np.ndarray:
    img = io.imread(img_path)
    img = rescale(
        img, scale_factor, anti_aliasing=True, preserve_range=True, channel_axis=2
    )

    return img


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")


model = StarDist2D(None, name="stardist-test", basedir="models")

sample_data = [
    (clone, sample)
    for clone in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, clone))
    for sample in os.listdir(os.path.join(DATA_DIR, clone))
    if os.path.isdir(os.path.join(DATA_DIR, clone, sample))
]

for item in tqdm(sample_data):
    clone, sample = item
    # print(clone, sample)
    img_path = os.path.join(DATA_DIR, clone, sample, "raw_data.tif")
    img = downscale_image(img_path)
    img = normalize(img, 1, 99.8, axis=(0, 1))

    labels, _ = model.predict_instances(img)  # type: ignore

    labels = rescale(labels, 10, anti_aliasing=False, order=0)

    # io.imsave("test_label.tif", labels)
    label_path = os.path.join(DATA_DIR, clone, sample, "stardist_label.tif")
    io.imsave(label_path, labels, check_contrast=False)
