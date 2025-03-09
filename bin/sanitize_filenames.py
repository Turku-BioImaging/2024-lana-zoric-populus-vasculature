"""
This script sanitizes filenames by removing or replacing certain characters and processes image and shapefile data.

The script performs the following tasks:
1. Sanitizes the clone and sample names by removing or replacing specific characters.
2. Writes the sanitized clone and sample names to separate text files.
3. Finds a matching shapefile in the specified directory based on the sanitized sample name.
4. Copies the matching shapefile to a new file named "shapes.csv".
5. Reads an image from the specified path, checks its dimensions and data type, and saves it as "raw-image.tif".

Usage:
    python sanitize_filenames.py --image-path <path_to_image> --clone <clone_name> --sample <sample_name> --shape-dir <path_to_shape_directory>

Arguments:
    --image-path : str : Path to the image file.
    --clone : str : Clone name to be sanitized.
    --sample : str : Sample name to be sanitized.
    --shape-dir : str : Directory containing shapefiles.

"""

import os
from skimage import io
import argparse
from glob import glob
import shutil


def _sanitize_name(name: str) -> str:
    name = (
        name.replace(" +", "")
        .replace("+", "")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        .rsplit(".", 1)[0]
    )

    return name


def _find_matching_shapefile(shape_dir: str, sample: str) -> str:
    shape_paths = glob(os.path.join(shape_dir, "*.csv"))
    for idx, shape_path in enumerate(shape_paths):
        path_fname = _sanitize_name(os.path.basename(shape_path))
        if path_fname == _sanitize_name(sample):
            return shape_paths[idx]

    raise ValueError(f"No matching shapefile found for {sample}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-path", type=str)
    parser.add_argument("--clone", type=str)
    parser.add_argument("--sample", type=str)
    parser.add_argument("--shape-dir", type=str)
    args = parser.parse_args()

    sanitized_clone_name = _sanitize_name(args.clone)
    sanitized_sample_name = _sanitize_name(args.sample)

    with open("clone-name.txt", "w") as f:
        f.write(sanitized_clone_name)
    with open("sample-name.txt", "w") as f:
        f.write(sanitized_sample_name)

    shapefile_path = _find_matching_shapefile(args.shape_dir, args.sample)
    shutil.copy(shapefile_path, "shapes.csv")

    raw_img = io.imread(args.image_path)
    assert raw_img.ndim == 3
    assert raw_img.shape[-1] == 3
    assert raw_img.dtype == "uint8"

    io.imsave("raw-image.tif", raw_img, check_contrast=False)
