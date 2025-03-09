"""
Experimental StarDist training script for custom data.
"""

import argparse
import os
from glob import glob

import numpy as np
from csbdeep.utils import normalize
from skimage import io
from skimage.transform import rescale
from stardist import (
    calculate_extents,
    fill_label_holes,
    gputools_available,
    random_label_cmap,
)
from stardist.matching import matching_dataset
from stardist.models import Config2D, StarDist2D
from tqdm import tqdm

np.random.seed(20)
lbl_cmap = random_label_cmap()


def downscale_image(img_path: str, scale_factor: float = 0.10) -> np.ndarray:
    img = io.imread(img_path)
    img = rescale(
        img, scale_factor, anti_aliasing=True, preserve_range=True, channel_axis=2
    )

    return img


def downscale_label(label_path: str, scale_factor: float = 0.10) -> np.ndarray:
    label_img = io.imread(label_path)
    label_img = rescale(label_img, scale_factor, anti_aliasing=False, order=0)

    return label_img


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

BATCH_SIZE = 12

parser = argparse.ArgumentParser()
parser.add_argument("--model-name", type=str, default="stardist-test-2")
args = parser.parse_args()

X = sorted(glob(os.path.join(IMG_DIR, "*.tif")))
Y = sorted(glob(os.path.join(LABEL_DIR, "*.tif")))

assert all([os.path.basename(x) == os.path.basename(y) for x, y in zip(X, Y)])

X = list(map(downscale_image, X))
Y = list(map(downscale_label, Y))

n_channel = 1 if X[0].ndim == 2 else X[0].shape[-1]

axis_norm = (0, 1)  # normalize channels independently
# axis_norm = (0,1,2) # normalize channels jointly
if n_channel > 1:
    print(
        "Normalizing image channels %s."
        % ("jointly" if axis_norm is None or 2 in axis_norm else "independently")
    )

X = [normalize(x, 1, 99.8, axis=axis_norm) for x in tqdm(X)]
Y = [fill_label_holes(y) for y in tqdm(Y)]

# split into train and validation sets
assert len(X) > 1, "not enough training data"
rng = np.random.RandomState(42)
ind = rng.permutation(len(X))
n_val = max(1, int(round(0.15 * len(ind))))
ind_train, ind_val = ind[:-n_val], ind[-n_val:]
X_val, Y_val = [X[i] for i in ind_val], [Y[i] for i in ind_val]
X_trn, Y_trn = [X[i] for i in ind_train], [Y[i] for i in ind_train]
print("number of images: %3d" % len(X))
print("- training:       %3d" % len(X_trn))
print("- validation:     %3d" % len(X_val))

# configure a stardist model
n_rays = 64
use_gpu = False and gputools_available()

grid = (2, 2)

conf = Config2D(
    n_rays=n_rays,
    grid=grid,
    use_gpu=use_gpu,
    n_channel_in=n_channel,
    train_batch_size=BATCH_SIZE,
)


model = StarDist2D(conf, name="stardist-test-2", basedir="models")

median_size = calculate_extents(list(Y), np.median)
fov = np.array(model._axes_tile_overlap("YX"))
print(f"median object size:      {median_size}")
print(f"network field of view :  {fov}")
if any(median_size > fov):
    print(
        "WARNING: median object size larger than field of view of the neural network."
    )


# data augmentation
def random_fliprot(img, mask):
    assert img.ndim >= mask.ndim
    axes = tuple(range(mask.ndim))
    perm = tuple(np.random.permutation(axes))
    img = img.transpose(perm + tuple(range(mask.ndim, img.ndim)))
    mask = mask.transpose(perm)
    for ax in axes:
        if np.random.rand() > 0.5:
            img = np.flip(img, axis=ax)
            mask = np.flip(mask, axis=ax)
    return img, mask


# def random_intensity_change(img):
#     img = img * np.random.uniform(0.6, 2) + np.random.uniform(-0.2, 0.2)
#     return img


def augmenter(x, y):
    """Augmentation of a single input/label image pair.
    x is an input image
    y is the corresponding ground-truth label image
    """
    x, y = random_fliprot(x, y)
    # x = random_intensity_change(x)
    # add some gaussian noise
    sig = 0.02 * np.random.uniform(0, 1)
    x = x + sig * np.random.normal(0, 1, x.shape)
    return x, y


model.train(
    X_trn,
    Y_trn,
    validation_data=(X_val, Y_val),
    augmenter=augmenter,
    epochs=200,
    steps_per_epoch=30,
)

# threshold optimization
model.optimize_thresholds(X_val, Y_val)

# evaluate detection performance
Y_val_pred = [
    model.predict_instances(
        x, n_tiles=model._guess_n_tiles(x), show_tile_progress=False
    )[0]
    for x in tqdm(X_val)
]


taus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
stats = [
    matching_dataset(Y_val, Y_val_pred, thresh=t, show_progress=False)
    for t in tqdm(taus)
]


stats[taus.index(0.5)]
