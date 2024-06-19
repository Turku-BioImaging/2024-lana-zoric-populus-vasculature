
# calculate area and parimeter of the label objects in the stardist predicted images

import os
from typing import Dict, List
from skimage import io
import polars as pl
from tqdm import tqdm
from skimage.measure import regionprops, label


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outputs")

def process_sample(data_dir: str, clone: str, sample: str) -> List[Dict]:
    mask = io.imread(os.path.join(data_dir, clone, sample, "stardist_label.tif"))
    assert mask.ndim == 2

    mask = mask > 0

    labeled_mask = label(mask)
    
    properties = regionprops(labeled_mask)
    object_sizes: List[Dict] = [
        {
            "clone": clone,
            "sample": sample,
            "label": prop.label,
            "size_pixels": prop.area,
            "perimeter_pixcels": prop.perimeter,
        }
        for prop in properties
    ] 
    return object_sizes

clone_data = [
    (clone, sample)
    for clone in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, clone))
    for sample in os.listdir(os.path.join(DATA_DIR, clone))
    if os.path.isdir(os.path.join(DATA_DIR, clone, sample))
]


all_object_sizes = []
for item in tqdm(clone_data):
    all_object_sizes.extend(process_sample(DATA_DIR, *item))  


df = pl.DataFrame(all_object_sizes)
df.write_csv(os.path.join(DATA_DIR, "object_sizes.csv"))