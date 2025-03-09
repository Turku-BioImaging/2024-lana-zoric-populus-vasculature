"""
Utility for writing data-list.txt, which is used
as the entry channel for Nextflow.
"""
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-data-dir", type=str, required=True)
    args = parser.parse_args()

    raw_data_dir = args.raw_data_dir

    clone_sample_data = [
        (clone, sample)
        for clone in os.listdir(raw_data_dir)
        if os.path.isdir(os.path.join(raw_data_dir, clone))
        for sample in os.listdir(os.path.join(raw_data_dir, clone))
        if os.path.isfile(os.path.join(raw_data_dir, clone, sample))
        and (sample.endswith(".tif") or sample.endswith(".bmp"))
    ]

    with open(os.path.join("..", "data-list.txt"), "w") as f:
        for clone, sample in clone_sample_data:
            f.write(f"{clone},{sample}\n")
