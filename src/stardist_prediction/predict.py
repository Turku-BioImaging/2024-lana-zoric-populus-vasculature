"""
StarDist prediction script.
"""

import os
import multiprocessing as mp
import numpy as np
import zarr
from csbdeep.utils import normalize
from skimage.segmentation import clear_border
from skimage.transform import rescale
from stardist.models import StarDist2D
from tqdm import tqdm
from zarr.hierarchy import Group
from typing import Any
from joblib import Parallel, delayed

MODEL_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "stardist_data", "models"
)

ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "zarr_data", "data.zarr"
)


def downscale_image(img: np.ndarray, scale_factor: float = 0.10) -> np.ndarray:
    return rescale(
        img, scale_factor, anti_aliasing=True, preserve_range=True, channel_axis=2
    )


def process_one_sample(zarr_path: str, clone: str, sample: str, model: StarDist2D):
    root: Group = zarr.open_group(zarr_path, mode="a")
    sample_path = f"{clone}/{sample}"
    raw_data: Any = root[sample_path]["raw_data"][:]
    img = downscale_image(raw_data)
    img = normalize(img, 1, 99.8, axis=(0, 1))

    labels, _ = model.predict_instances(img)  # type: ignore
    labels = clear_border(labels)
    labels = rescale(labels, 10, anti_aliasing=False, order=0, preserve_range=True)

    assert (
        raw_data.shape[:2] == labels.shape
    ), f"Shape mismatch: {raw_data.shape} != {labels.shape}"

    if f"{sample_path}/stardist_labels" in root:
        del root[f"{sample_path}/stardist_labels"]

    dataset = root.create_dataset(f"{sample_path}/stardist_labels", data=labels)
    dataset.attrs.update(
        {
            "description": "StarDist prediction labels",
            "clone": clone,
            "sample": sample,
            "author": "Turku BioImaging",
            "resolution": {"unit": "microns/pixel", "x": 0.0878, "y": 0.0878},
        }
    )


def main():
    model = StarDist2D(None, name="stardist-test-2", basedir=MODEL_DIR)  # type: ignore
    root: Group = zarr.open_group(ZARR_PATH, mode="a")

    clone_sample_data = [
        (clone, sample)
        for clone in list(root.keys())
        for sample in list(root[clone].keys())  # type: ignore
    ]

    Parallel(n_jobs=(mp.cpu_count() // 2))(
        delayed(process_one_sample)(ZARR_PATH, clone, sample, model)
        for clone, sample in tqdm(clone_sample_data)
    )


if __name__ == "__main__":
    main()


class StarDistPredictor:
    model = StarDist2D(None, name="stardist-test-2", basedir=MODEL_DIR)

    def __init__(self, model_dir: str = MODEL_DIR, zarr_path: str = ZARR_PATH):
        self.model = StarDist2D(None, name="stardist-test-2", basedir=model_dir)
        self.zarr_path = zarr_path

    def predict_sample(self, clone: str, sample: str):
        process_one_sample(self.zarr_path, clone, sample, self.model)

    def predict_all(self, n_jobs: int = (mp.cpu_count() // 2)):
        root: Group = zarr.open_group(self.zarr_path, mode="a")

        clone_sample_data = [
            (clone, sample)
            for clone in list(root.keys())
            for sample in list(root[clone].keys())  # type: ignore
        ]

        Parallel(n_jobs=n_jobs)(
            delayed(process_one_sample)(self.zarr_path, clone, sample, self.model)
            for clone, sample in tqdm(clone_sample_data)
        )
