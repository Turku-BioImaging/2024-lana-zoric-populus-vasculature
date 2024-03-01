import os
import shutil

import numpy as np
import zarr
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from skimage.transform import rescale
from tqdm import tqdm

ZARR_PATH = os.path.join(
    os.path.dirname(__file__), "..", "zarr_data", "plant-vasculatur-data.zarr"
)

WORK_DIR = os.path.join(os.path.dirname(__file__), "..", "workdir")

SAM_MODEL_TYPE = "vit_l"
SAM_CHECKPOINT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "sam_checkpoints", "sam_vit_l_0b3195.pth"
)
SAM_DEVICE = "cuda"
AREA_MIN_THRESHOLD = 2000
AREA_MAX_THRESHOLD = 25000


if __name__ == "__main__":
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    os.makedirs(WORK_DIR)

    # init sam
    sam = sam_model_registry[SAM_MODEL_TYPE](SAM_CHECKPOINT_PATH)
    sam.to(device=SAM_DEVICE)
    mask_generator = SamAutomaticMaskGenerator(sam)

    root = zarr.open(ZARR_PATH, mode="a")

    clones = list(root.keys())
    for clone in clones:

        samples = list(root[clone].keys())

        print(f"Processing clone: {clone}, samples: {len(samples)}")
        for s in tqdm(samples):
            img = np.array(root[clone][s]["raw_data"])

            img = rescale(img, 0.25, anti_aliasing=True, channel_axis=2)
            img = (img * 255).astype(np.uint8)

            predictions = mask_generator.generate(img)
            filtered_predictions = sorted(
                predictions, key=(lambda x: x["area"]), reverse=True
            )

            labels = []

            for pred in filtered_predictions:
                if (
                    pred["area"] > AREA_MIN_THRESHOLD
                    and pred["area"] < AREA_MAX_THRESHOLD
                ):
                    labels.append(rescale(pred["segmentation"], 4, order=0))

            labels = np.array(labels, dtype=bool)

            if root[clone][s].get("segmentation", {}).get("sam_prediction", False):
                del root[clone][s]["segmentation"]["sam_prediction"]

            l_dataset = root.create_dataset(
                f"{clone}/{s}/segmentation/sam_prediction", data=labels
            )
            l_dataset.attrs["description"] = "Binary mask derived from SAM predictor."
            l_dataset.attrs["author"] = "Turku BioImaging"
