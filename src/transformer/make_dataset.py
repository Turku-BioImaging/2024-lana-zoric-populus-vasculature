from glob import glob
import numpy as np

import os
from datasets import Dataset, DatasetDict
from skimage.transform import rescale
from PIL import Image


def load_and_preprocess_image(img_path, label_path):
    img = Image.open(img_path)
    label = Image.open(label_path)

    img = np.array(img)
    img = rescale(
        img, 0.25, anti_aliasing=True, channel_axis=-1, order=1, preserve_range=True
    )

    mask = np.where(np.array(label) > 0, 1, 0).astype(bool).astype(np.float32)
    mask = rescale(mask, 0.25, anti_aliasing=False, order=0, preserve_range=True)
    return {"image": img, "mask": mask}


IMG_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stardist_data",
    "images_for_annotation",
    "images",
)

LABEL_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "stardist_data", "labels"
)

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "datasets")

img_paths = sorted(glob(os.path.join(IMG_DIR, "*.tif")))
label_paths = sorted(glob(os.path.join(LABEL_DIR, "*.tif")))

assert len(img_paths) == len(label_paths)
train_split = int(0.7 * len(img_paths))
val_split = int(0.9 * len(img_paths))

train_dataset = Dataset.from_dict(
    {"img_path": img_paths[:train_split], "label_path": label_paths[:train_split]}
)
val_dataset = Dataset.from_dict(
    {
        "img_path": img_paths[train_split:val_split],
        "label_path": label_paths[train_split:val_split],
    }
)
test_dataset = Dataset.from_dict(
    {"img_path": img_paths[val_split:], "label_path": label_paths[val_split:]}
)

# Map the load_and_preprocess_image function to each dataset
train_dataset = train_dataset.map(
    lambda x: load_and_preprocess_image(x["img_path"], x["label_path"]),
    remove_columns=["img_path", "label_path"],
)
val_dataset = val_dataset.map(
    lambda x: load_and_preprocess_image(x["img_path"], x["label_path"]),
    remove_columns=["img_path", "label_path"],
)
test_dataset = test_dataset.map(
    lambda x: load_and_preprocess_image(x["img_path"], x["label_path"]),
    remove_columns=["img_path", "label_path"],
)

dataset_dict = DatasetDict(
    {"train": train_dataset, "validation": val_dataset, "test": test_dataset}
)

train_dataset.save_to_disk(os.path.join(DATASET_DIR, "train"))
val_dataset.save_to_disk(os.path.join(DATASET_DIR, "val"))
test_dataset.save_to_disk(os.path.join(DATASET_DIR, "test"))
