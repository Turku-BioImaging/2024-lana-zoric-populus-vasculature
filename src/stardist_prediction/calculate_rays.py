"""
Calculate and plot the optimum number of rays to to use. Images / label pairs are downscaled to 10% of their original size.
"""

import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage.transform import rescale
from stardist import fill_label_holes, random_label_cmap, relabel_image_stardist
from stardist.matching import matching_dataset
from tqdm import tqdm

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


np.random.seed(7752)
lbl_cmap = random_label_cmap()

X = sorted(glob(os.path.join(IMG_DIR, "*.tif")))
Y = sorted(glob(os.path.join(LABEL_DIR, "*.tif")))


assert all([os.path.basename(x) == os.path.basename(y) for x, y in zip(X, Y)])


X = list(map(downscale_image, X))
Y = list(map(downscale_label, Y))


i = min(4, len(X) - 1)
img, lbl = X[i], fill_label_holes(Y[i])
assert img.ndim in (2, 3)
img = img if img.ndim == 2 else img[..., :3]
# assumed axes ordering of img and lbl is: YX(C)


n_rays = [2**i for i in range(2, 8)]
scores = []
for r in tqdm(n_rays):
    Y_reconstructed = [relabel_image_stardist(lbl, n_rays=r) for lbl in Y]
    mean_iou = matching_dataset(
        Y, Y_reconstructed, thresh=0, show_progress=False
    ).mean_true_score

    scores.append(mean_iou)

plt.figure(figsize=(8, 5))
plt.plot(n_rays, scores, "o-")
plt.xlabel("Number of rays for star-convex polygon")
plt.ylabel("Reconstruction score (mean intersection over union)")
plt.title(
    "Accuracy of ground truth reconstruction (should be > 0.8 for a reasonable number of rays)"
)
plt.show()
