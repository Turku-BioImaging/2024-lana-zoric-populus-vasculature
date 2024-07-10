"""
Utility function for copying raw data from the original folders into our own output hierarchy.
"""

import os
import re

from skimage import io


def copy_raw_data_to_output(
    raw_data_dir: str, output_dir: str, clone_name: str, sample_name: str, **kwargs
) -> None:
    assert os.path.isdir(raw_data_dir)
    assert os.path.isdir(output_dir)

    # sanitize output filenames
    sanitized_clone_name = clone_name.replace(" ", "").replace("-", "_")
    sanitized_clone_name = re.sub(r"\W+", "", sanitized_clone_name)

    sanitized_sample_name = (
        sample_name.replace(" ", "_").replace("-", "_").replace(".tif", "")
    )

    sanitized_sample_name = re.sub(r"\W+", "", sanitized_sample_name)

    if "overwrite" in kwargs.items() and kwargs["overwrite"] is True:
        file_path = os.path.join(
            output_dir, sanitized_clone_name, sanitized_sample_name, "raw_data.tif"
        )
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.makedirs(
        os.path.join(output_dir, sanitized_clone_name, sanitized_sample_name),
        exist_ok=True,
    )

    # get raw data image and copy to output
    raw_data_path = os.path.join(raw_data_dir, clone_name, sample_name)
    output_fpath = os.path.join(
        output_dir, sanitized_clone_name, sanitized_sample_name, "raw_data.tif"
    )

    raw_data = io.imread(raw_data_path)
    assert raw_data.ndim == 3, raw_data.shape[2] == 3
    io.imsave(output_fpath, raw_data)
