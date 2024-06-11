import os
import pandas as pd
from skimage import io  # type: ignore
from skimage.util import img_as_ubyte
from skimage.morphology import remove_small_objects
from skimage.measure import label, regionprops
from tqdm import tqdm
from typing import List, Dict

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")
MIN_OBJECT_SIZE = 20000


def process_sample(data_dir: str, clone: str, sample: str) -> List[Dict]:
    mask = io.imread(os.path.join(data_dir, clone, sample, "binary_mask.tif"))
    assert mask.ndim == 2

    mask = mask > 0
    filtered_mask = remove_small_objects(mask, min_size=MIN_OBJECT_SIZE)

    labeled_image = label(filtered_mask)

    properties = regionprops(labeled_image)
    object_sizes: List[Dict] = [
        {
            "clone": clone,
            "sample": sample,
            "label": prop.label,
            "size_pixels": prop.area,
        }
        for prop in properties
    ]

    io.imsave(
        os.path.join(data_dir, clone, sample, "filtered_binary_mask.tif"),
        img_as_ubyte(filtered_mask),
        check_contrast=False,
    )
    io.imsave(
        os.path.join(data_dir, clone, sample, "object_labels.tif"),
        labeled_image,
        check_contrast=False,
    )

    return object_sizes


sample_data = [
    (clone, sample)
    for clone in os.listdir(DATA_PATH)
    if os.path.isdir(os.path.join(DATA_PATH, clone))
    for sample in os.listdir(os.path.join(DATA_PATH, clone))
    if os.path.isdir(os.path.join(DATA_PATH, clone, sample))
]


all_object_sizes = []
for item in tqdm(sample_data):
    all_object_sizes.extend(process_sample(DATA_PATH, *item))

df = pd.DataFrame(all_object_sizes)
df.to_csv(os.path.join(DATA_PATH, "object_sizes.csv"), index=False)
