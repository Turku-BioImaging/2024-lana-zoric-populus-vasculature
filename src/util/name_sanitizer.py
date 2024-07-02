"""
Defines a function that sanitizes a name by removing all non-alphanumeric characters.
"""

import os


def sanitize_name(name: str) -> str:
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


def find_matching_shapefile(shape_paths: list, sample: str) -> str:
    """
    Finds a matching shapefile path based on a given sample name.

    Args:
        shape_paths (list): A list of shapefile paths to search through.
        sample (str): The sample name to match.

    Returns:
        str: The path of the matching shapefile, or None if no match is found.
    """
    for idx, shape_path in enumerate(shape_paths):
        path_fname = os.path.basename(shape_path)
        sanitized_fname = sanitize_name(path_fname)
        if sanitized_fname == sample:
            return shape_paths[idx]
    return None
