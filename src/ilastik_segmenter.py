"""
Defines IlastikSegmenter class. Expected input are downsampled images
of the Populus clones. The output is a rough binary mask of the vascular structures,
which will require further filtering.
"""

import os
from typing import Any, Tuple

import numpy as np
from ilastik.experimental.api import from_project_file
from skimage import io  # type: ignore
from skimage.transform import rescale
from skimage.util import img_as_ubyte
from xarray import DataArray

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "ilastik_model")
MODEL_NAME = "model-2024-06-06"


class IlastikSegmenter:
    pipeline = from_project_file(os.path.join(MODEL_DIR, MODEL_NAME + ".ilp"))

    def segment_one(self, clone_data: Tuple[str, str, str], overwrite: bool = True):
        data_dir, clone, sample = clone_data

        mask_path = os.path.join(data_dir, clone, sample, "binary_mask.tif")
        if overwrite is False and os.path.isfile(mask_path):
            return

        img = io.imread(os.path.join(data_dir, clone, sample, "raw_data.tif"))
        assert img.ndim == 3, img.shape[2] == 3
        img: np.ndarray = img_as_ubyte(
            rescale(img, 0.5, anti_aliasing=True, order=1, channel_axis=2)
        )
        data_array: Any = DataArray(img, dims=["y", "x", "c"])
        pred: np.ndarray = self.pipeline.predict(data_array).values
        pred = img_as_ubyte(pred[..., 1] >= 0.5)

        pred = img_as_ubyte(rescale(pred, 2, anti_aliasing=True, order=0))

        io.imsave(mask_path, pred, check_contrast=False)
