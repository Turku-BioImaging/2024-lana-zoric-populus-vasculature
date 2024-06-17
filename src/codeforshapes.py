# import os
# from glob import glob
# import polars as pl
# from constants import CLASS_LABELS
# from shapely.geometry import Polygon
# from rasterio.features import rasterize
# from skimage import io

# SHAPE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "stardist_data", "shapes")


# slides = list(root.keys())

# for slide in slides:
#     # check if a shape file exists for white matter
#     shape_file_path = os.path.join(SHAPE_DIR, slide, ".csv")
#     df = (
#         pl.read_csv(shape_file_path)
#         .select(["index", "axis-1", "axis-2"])
#         .rename({"axis-1": "y", "axis-2": "x"})
#     )

#     df = df.with_columns(
#         df["y"].map_elements(round, return_dtype=pl.Int32).alias("y"),
#         df["x"].map_elements(round, return_dtype=pl.Int32).alias("x"),
#     ).group_by(["index"])

    
#     for name, polygon_data in df:
#         polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
#         mask = rasterize(
#             [polygon],
#             out_shape=mask_image.shape,
#         )

#         label_img[mask == 1] = CLASS_LABELS["white_matter"]


#     io.imsave('label_img.tif', label_img)
#     break



import os
import numpy as np
import polars as pl
from shapely.geometry import Polygon
from rasterio.features import rasterize
from skimage import io

# Constants
CLASS_LABELS = {"vessical_obj": 1}  # Dictionary to map class names to integer labels

# Path to shape directory
SHAPE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "stardist_data", "shapes")

# # Assuming `root` and `mask_image` are defined elsewhere in your context
# slides = list(root.keys())

# Initialize root and slides
root = {}  # Assuming this would be populated with actual data elsewhere in your context
slides = list(root.keys()) if root else []  # Use an empty list if root is not defined

# Assuming mask_image is defined elsewhere in your context
mask_image = np.zeros((1024, 1024), dtype=np.uint8)      # Example shape, adjust as necessary

for slide in slides:
    # Construct the shape file path
    shape_file_path = os.path.join(SHAPE_DIR, slide + ".csv")  # Ensure the correct file extension
    if not os.path.exists(shape_file_path):
        print(f"No shape file for slide: {slide}")
        continue
    
    # Read and process the shape CSV file
    df = (
        pl.read_csv(shape_file_path)
        .select(["index", "axis-1", "axis-2"])
        .rename({"axis-1": "y", "axis-2": "x"})
    )

    # Round the coordinates and group by 'index'
    df = df.with_columns(
        df["y"].map_elements(round, return_dtype=pl.Int32).alias("y"),
        df["x"].map_elements(round, return_dtype=pl.Int32).alias("x")
    ).groupby("index").agg([
        pl.col("x").list().alias("x"),
        pl.col("y").list().alias("y")
    ])
    
    # Initialize the mask image with the same shape as the original image
    mask_image = np.zeros(mask_image.shape, dtype=np.uint8)
    
    # Process each polygon
    for polygon_data in df.iter_rows():
        polygon = Polygon(zip(polygon_data["x"], polygon_data["y"]))
        mask = rasterize(
            [(polygon, 1)],  # Rasterize the polygon with a value of 1
            out_shape=mask_image.shape,
            fill=0,
            transform=None,  # Use an appropriate transform if needed
            dtype=np.uint8
        )

        # Assign the class label to the mask
        mask_image[mask == 1] = CLASS_LABELS["vessical_obj"]

    # Save the labeled image
    io.imsave(f'{slide}_label_img.tif', mask_image)
    break  # Process only the first slide; remove this if you want to process all slides
