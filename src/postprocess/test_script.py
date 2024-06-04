from skimage import io, img_as_bool, img_as_ubyte
import matplotlib.pyplot as plt
from skimage.morphology import remove_small_objects
import os
from glob import glob

# # Load the image
# # image_path = r'C:\Users\ramish.bibi\Desktop\raw_data\ilastik_binary_masks\129-81+  Binary\processed_129-81 1a_Simple Segmentation.tif'  # Replace with your image path
# # image_path = os.path.join(
# #     os.path.dirname(__file__),
# #     "..",
# #     "..",
# #     "data",
# #     "raw_data",
# #     "ilastik_binary_masks",
# #     "129-81+ Binary",
# #     "processed_129-81 1a_Simple Segmentation.tif",
# # )
# # image = io.imread(image_path)

# # image_paths = sorted(
# #   glob(
# #        os.path.join(
# #           os.path.dirname(__file__),
# #            "..",
# #            "..",
# #           "data",
# #            "raw_data",
# #            "ilastik_binary_masks",
# #            "**",
# #            "*Simple Segmentation.tif",
# #        )
# #    )
# # )


# # for i in image_paths:
# #   mask = img_as_bool(io.imread(i))
# #  print(os.path.basename(i))
# # print(mask.shape, mask.dtype)
# # plt.imshow(mask)
# # plt.show()

# #   io.imsave("mask_1.tif", mask)

# #  mask_filtered = remove_small_objects(mask, min_size=1000)

# #  io.imsave("mask_2.tif", mask_filtered)

# # plt.imshow(mask_filtered)
# # plt.show()

# # break


# # Display the image
# # plt.imshow(image)
# # plt.axis("off")  # Hide axes
# # plt.show()


# # new code for saving filter mask in raw data folder


# # Define the path to the directory containing the original masks
# original_masks_dir = os.path.join(
#     "..", "..", "data", "raw_data", "ilastik_binary_masks"
# )

# # Define the path to the existing folder
# existing_folder_path = os.path.join("..", "..", "data", "raw_data", "Filter_RSO_images")

# # Create the existing folder if it doesn't exist
# os.makedirs(existing_folder_path, exist_ok=True)

# # Glob for the image paths
# image_paths = sorted(
#     glob(
#         os.path.join(
#             original_masks_dir,
#             "**",
#             "*Simple Segmentation.tif",
#         )
#     )
# )


# # Process each image
# for i in image_paths:
#     # Read the original mask
#     mask = img_as_bool(io.imread(i))

#     # Get the filename
#     filename = os.path.basename(i)

#     # Print the filename
#     print(filename)

#     # Save the original mask in the existing folder
#     io.imsave(
#         os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask)
#     )

#     # # Remove small objects from the mask
#     # mask_filtered = remove_small_objects(mask, min_size=2500)

#     # # Save the filtered mask in the existing folder
#     # io.imsave(
#     #     os.path.join(existing_folder_path, "filtered_" + filename),
#     #     img_as_ubyte(mask_filtered),
#     # )



# """ # """ # Modify for connecting component labelling


# import os
# import numpy as np
# import warnings
# from skimage import io, img_as_bool, img_as_ubyte, img_as_uint
# from skimage.morphology import remove_small_objects
# from skimage.measure import label
# from glob import glob

# # Suppress specific warnings
# warnings.filterwarnings("ignore", category=UserWarning, message="Downcasting int32 to uint16 without scaling because max value")
# warnings.filterwarnings("ignore", category=UserWarning, message="is a low contrast image")

# # Define the path to the directory containing the original masks
# original_masks_dir = os.path.join('..', '..', "data", "raw_data", "ilastik_binary_masks")

# # Define the path to the existing folder
# existing_folder_path = os.path.join('..', '..', "data", "raw_data", "Filter_RSO_images")

# # Create the existing folder if it doesn't exist
# os.makedirs(existing_folder_path, exist_ok=True)

# # Glob for the image paths
# image_paths = sorted(
#     glob(
#         os.path.join(
#             original_masks_dir,
#             "**",
#             "*Simple Segmentation.tif",
#         )
#     )
# )

# # Process each image
# for i in image_paths:
#     # Read the original mask
#     mask = img_as_bool(io.imread(i))
    
#     # Get the filename
#     filename = os.path.basename(i)
    
#     # Print the filename
#     print(filename)
    
#     # Save the original mask in the existing folder
#     io.imsave(os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask))
    
#     # Remove small objects from the mask
#     mask_filtered = remove_small_objects(mask, min_size=2500)
    
#     # Save the filtered mask in the existing folder
#     io.imsave(os.path.join(existing_folder_path, "filtered_" + filename), img_as_ubyte(mask_filtered))
    
#     # Perform connected component labeling on the filtered mask only
#     labeled_mask = label(mask_filtered)
    
#     # Save the labeled mask in the existing folder
#     io.imsave(os.path.join(existing_folder_path, "labeled_" + filename), img_as_uint(labeled_mask))

#     break 



# modify for size measure and size distribution plot of labelled images

import os
import numpy as np
import warnings
from skimage import io, img_as_bool, img_as_ubyte, img_as_uint
from skimage.morphology import remove_small_objects
from skimage.measure import label, regionprops
from glob import glob
import csv
import matplotlib.pyplot as plt

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Downcasting int32 to uint16 without scaling because max value")
warnings.filterwarnings("ignore", category=UserWarning, message="is a low contrast image")

# Define the path to the directory containing the original masks
original_masks_dir = os.path.join('..', '..', "data", "raw_data", "ilastik_binary_masks")

# Define the path to the existing folder
existing_folder_path = os.path.join('..', '..', "data", "raw_data", "Filter_RSO_images")

# Create the existing folder if it doesn't exist
os.makedirs(existing_folder_path, exist_ok=True)

# Glob for the image paths
image_paths = sorted(
    glob(
        os.path.join(
            original_masks_dir,
            "**",
            "*Simple Segmentation.tif",
        )
    )
)

# Path to save the CSV file
csv_path = os.path.join(existing_folder_path, "label_properties.csv")

# List to store areas for plotting
areas = []

# Write properties to CSV file
with open(csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Filename', 'Label', 'Centroid', 'Area', 'BoundingBox']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    # Process each image
    for i in image_paths:
        # Read the original mask
        mask = img_as_bool(io.imread(i))
        
        # Get the filename
        filename = os.path.basename(i)
        
        # Print the filename
        print(filename)
        
        # Save the original mask in the existing folder
        io.imsave(os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask))
        
        # Remove small objects from the mask
        mask_filtered = remove_small_objects(mask, min_size=2500)
        
        # Save the filtered mask in the existing folder
        io.imsave(os.path.join(existing_folder_path, "filtered_" + filename), img_as_ubyte(mask_filtered))
        
        # Perform connected component labeling on the filtered mask only
        labeled_mask = label(mask_filtered)
        
        # Save the labeled mask in the existing folder
        io.imsave(os.path.join(existing_folder_path, "labeled_" + filename), img_as_uint(labeled_mask))
        
        # Measure properties of labeled regions
        properties = regionprops(labeled_mask)
        
        # Write properties of each labeled object to the CSV file and collect areas for plotting
        for prop in properties:
            writer.writerow({
                'Filename': filename,
                'Label': prop.label,
                'Centroid': prop.centroid,
                'Area': prop.area,
                'BoundingBox': prop.bbox
            })
            areas.append(prop.area)

# Plot the distribution of sizes
plt.hist(areas, bins=50, edgecolor='black')
plt.title('Distribution of Object Sizes')
plt.xlabel('Size (Area)')
plt.ylabel('Frequency')
plt.show()
