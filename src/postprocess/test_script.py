# from skimage import io, img_as_bool, img_as_ubyte
# import matplotlib.pyplot as plt
# from skimage.morphology import remove_small_objects
# import os
# from glob import glob

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

# image_paths = sorted(
#   glob(
#        os.path.join(
#           os.path.dirname(__file__),
#            "..",
#            "..",
#           "data",
#            "outputs",
     
#            "**",
#            "*binary_mask.tif",
#        )
#    )
# )


# for i in image_paths:
#   mask = img_as_bool(io.imread(i))
#   print(os.path.basename(i))
# print(mask.shape, mask.dtype)
# plt.imshow(mask)
# plt.show()

# io.imsave("mask_1.tif", mask)

# mask_filtered = remove_small_objects(mask, min_size=2000)

# io.imsave("mask_2.tif", mask_filtered)

# plt.imshow(mask_filtered)
# plt.show()

#break


# # Display the image
# # plt.imshow(image)
# # plt.axis("off")  # Hide axes
# # plt.show()


# # new code for saving filter mask in raw data folder


# # Define the path to the directory containing the original masks
# original_masks_dir = os.path.join(
#     "..", "..", "data", "raw_data", "ilastik_binary_masks"
# )

# path to the folder containing images
# input_folder = os.path.join(
#     os.path.dirname(__file__), "..", "..", "data", "outputs"
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



# # modify for size measure and size distribution plot of labelled images

# import os
# import numpy as np
# import warnings
# from skimage import io, img_as_bool, img_as_ubyte, img_as_uint
# from skimage.morphology import remove_small_objects
# from skimage.measure import label, regionprops
# from glob import glob
# import csv
# import matplotlib.pyplot as plt

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

# # Path to save the CSV file
# csv_path = os.path.join(existing_folder_path, "label_properties.csv")

# # List to store areas for plotting
# areas = []

# # Write properties to CSV file
# with open(csv_path, 'w', newline='') as csvfile:
#     fieldnames = ['Filename', 'Label', 'Centroid', 'Area', 'BoundingBox']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
    
#     # Process each image
#     for i in image_paths:
#         # Read the original mask
#         mask = img_as_bool(io.imread(i))
        
#         # Get the filename
#         filename = os.path.basename(i)
        
#         # Print the filename
#         print(filename)
        
#         # Save the original mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask))
        
#         # Remove small objects from the mask
#         mask_filtered = remove_small_objects(mask, min_size=2500)
        
#         # Save the filtered mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "filtered_" + filename), img_as_ubyte(mask_filtered))
        
#         # Perform connected component labeling on the filtered mask only
#         labeled_mask = label(mask_filtered)
        
#         # Save the labeled mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "labeled_" + filename), img_as_uint(labeled_mask))
        
#         # Measure properties of labeled regions
#         properties = regionprops(labeled_mask)
        
#         # Write properties of each labeled object to the CSV file and collect areas for plotting
#         for prop in properties:
#             writer.writerow({
#                 'Filename': filename,
#                 'Label': prop.label,
#                 'Centroid': prop.centroid,
#                 'Area': prop.area,
#                 'BoundingBox': prop.bbox
#             })
#             areas.append(prop.area)

# # Plot the distribution of sizes
# plt.hist(areas, bins=50, edgecolor='black')
# plt.title('Distribution of Object Sizes')
# plt.xlabel('Size (Area)')
# plt.ylabel('Frequency')
# plt.show()


# # modify to remove large objects


# import os
# import numpy as np
# import warnings
# from skimage import io, img_as_bool, img_as_ubyte, img_as_uint
# from skimage.morphology import remove_small_objects, label
# from skimage.measure import regionprops
# from glob import glob
# import csv
# import matplotlib.pyplot as plt

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

# # Custom function to remove large objects
# def remove_large_objects(ar, max_size=100000):
#     labeled_ar = label(ar)
#     props = regionprops(labeled_ar)
#     for prop in props:
#         if prop.area > max_size:
#             labeled_ar[labeled_ar == prop.label] = 0
#     return labeled_ar > 0

# # Path to save the CSV file
# csv_path = os.path.join(existing_folder_path, "label_properties.csv")

# # List to store areas for plotting
# areas = []

# # Write properties to CSV file
# with open(csv_path, 'w', newline='') as csvfile:
#     fieldnames = ['Filename', 'Label', 'Centroid', 'Area', 'BoundingBox']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
    
#     # Process each image
#     for i in image_paths:
#         # Read the original mask
#         mask = img_as_bool(io.imread(i))
        
#         # Get the filename
#         filename = os.path.basename(i)
        
#         # Print the filename
#         print(filename)
        
#         # Save the original mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask))
        
#         # Remove small objects from the mask
#         mask_filtered = remove_small_objects(mask, min_size=2500)
        
#         # Remove large objects from the mask
#         mask_filtered = remove_large_objects(mask_filtered, max_size=100000)
        
#         # Save the filtered mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "filtered_" + filename), img_as_ubyte(mask_filtered))
        
#         # Perform connected component labeling on the filtered mask only
#         labeled_mask = label(mask_filtered)
        
#         # Save the labeled mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "labeled_" + filename), img_as_uint(labeled_mask))
        
#         # Measure properties of labeled regions
#         properties = regionprops(labeled_mask)
        
#         # Write properties of each labeled object to the CSV file and collect areas for plotting
#         for prop in properties:
#             writer.writerow({
#                 'Filename': filename,
#                 'Label': prop.label,
#                 'Centroid': prop.centroid,
#                 'Area': prop.area,
#                 'BoundingBox': prop.bbox
#             })
#             areas.append(prop.area)

# # Plot the distribution of sizes
# plt.hist(areas, bins=50, edgecolor='black')
# plt.title('Distribution of Object Sizes')
# plt.xlabel('Size (Area)')
# plt.ylabel('Frequency')
# plt.show()

# Modify for removing elongated remove_small_objects

# import os
# import numpy as np
# import warnings
# from skimage import io, img_as_bool, img_as_ubyte, img_as_uint
# from skimage.morphology import remove_small_objects, label
# from skimage.measure import regionprops
# from glob import glob
# import csv
# import matplotlib.pyplot as plt

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

# # Custom function to remove large and non-round objects
# def remove_large_and_nonround_objects(ar, max_size=100000, max_eccentricity=0.995):
#     labeled_ar = label(ar)
#     props = regionprops(labeled_ar)
#     for prop in props:
#         if prop.area > max_size or prop.eccentricity > max_eccentricity:
#             labeled_ar[labeled_ar == prop.label] = 0
#     return labeled_ar > 0

# # Path to save the CSV file
# csv_path = os.path.join(existing_folder_path, "label_properties.csv")

# # List to store areas for plotting
# areas = []

# # Write properties to CSV file
# with open(csv_path, 'w', newline='') as csvfile:
#     fieldnames = ['Filename', 'Label', 'Centroid', 'Area', 'BoundingBox', 'Eccentricity']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
    
#     # Process each image
#     for i in image_paths:
#         # Read the original mask
#         mask = img_as_bool(io.imread(i))
        
#         # Get the filename
#         filename = os.path.basename(i)
        
#         # Print the filename
#         print(filename)
        
#         # Save the original mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "original_" + filename), img_as_ubyte(mask))
        
#         # Remove small objects from the mask
#         mask_filtered = remove_small_objects(mask, min_size=2500)
        
#         # Remove large and non-round objects from the mask
#         mask_filtered = remove_large_and_nonround_objects(mask_filtered, max_size=100000, max_eccentricity=0.8)
        
#         # Save the filtered mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "filtered_" + filename), img_as_ubyte(mask_filtered))
        
#         # Perform connected component labeling on the filtered mask only
#         labeled_mask = label(mask_filtered)
        
#         # Save the labeled mask in the existing folder
#         io.imsave(os.path.join(existing_folder_path, "labeled_" + filename), img_as_uint(labeled_mask))
        
#         # Measure properties of labeled regions
#         properties = regionprops(labeled_mask)
        
#         # Write properties of each labeled object to the CSV file and collect areas for plotting
#         for prop in properties:
#             writer.writerow({
#                 'Filename': filename,
#                 'Label': prop.label,
#                 'Centroid': prop.centroid,
#                 'Area': prop.area,
#                 'BoundingBox': prop.bbox,
#                 'Eccentricity': prop.eccentricity
#             })
#             areas.append(prop.area)

# # Plot the distribution of sizes
# plt.hist(areas, bins=50, edgecolor='black')
# plt.title('Distribution of Object Sizes')
# plt.xlabel('Size (Area)')
# plt.ylabel('Frequency')
# plt.show()


# # Remove small objects and generate labelled images after new ilastik model for first image 

# import os
# import pandas as pd
# from skimage import io, img_as_ubyte
# from skimage.morphology import remove_small_objects
# from skimage.measure import label, regionprops

# def process_image(input_image_path, output_image_path, labeled_image_path, min_size):
#     try:
#         # Read the image
#         image = io.imread(input_image_path)
        
#         # Ensure the image is binary
#         binary_image = image > 0

#         # Remove small objects
#         filtered_image = remove_small_objects(binary_image, min_size=min_size)

#         # Perform connected component labeling on the filtered image
#         labeled_image = label(filtered_image)
        
#         # Collect sizes of objects in the labeled image
#         properties = regionprops(labeled_image)
#         object_sizes = [{'filename': input_image_path, 'label': prop.label, 'size': prop.area} for prop in properties]

        
#         # Convert images to unsigned 8-bit format for saving
#         filtered_image_ubyte = img_as_ubyte(filtered_image)
#         labeled_image_ubyte = img_as_ubyte(labeled_image)
        
#         # Save the cleaned image
#         io.imsave(output_image_path, img_as_ubyte(filtered_image))
#         # Save the labeled image
#         io.imsave(labeled_image_path, labeled_image_ubyte)

#         print(f"Processed and saved filtered image at: {output_image_path}")
#         print(f"Processed and saved labeled image at: {labeled_image_path}")
        
#         return object_sizes

#     except Exception as e:
#         print(f"Error processing file {input_image_path}: {e}")
#         return []

# # # Replace with the path to your folder containing images
# input_folder = os.path.join(
#     os.path.dirname(__file__), "..", "..", "data", "outputs"
# )   
# min_size = 5000  # Minimum size of small objects to be removed, adjust as needed
# csv_output_path = 'object_sizes.csv'  # Path to save the CSV file

# all_object_sizes = []

# # Process all images in the folder
# processed = False
# for dirpath, dirnames, filenames in os.walk(input_folder):
#     for filename in filenames:
#         if filename.lower().endswith(("binary_mask.tif")):
#             input_image_path = os.path.join(dirpath, filename)
            
#             # Create a new filename to save the cleaned image
#             name, ext = os.path.splitext(filename)
#             filtered_filename = f"filtered_{name}{ext}"
#             labeled_filename = f"label_{name}{ext}"
#             filtered_file_path = os.path.join(dirpath, filtered_filename)
#             labeled_file_path = os.path.join(dirpath, labeled_filename)
            
#             object_sizes = process_image(input_image_path, filtered_file_path, labeled_file_path, min_size)
#             all_object_sizes.extend(object_sizes)

#             processed = True
#             break
#     if processed:
#         break
    
    
#     # Save object sizes to a CSV file
# df = pd.DataFrame(all_object_sizes)
# df.to_csv(csv_output_path, index=False)

# print(f"Object sizes saved to {csv_output_path}")





# Remove small objects and generate labelled images after new ilastik model for all images

import os
import pandas as pd
from skimage import io, img_as_ubyte
from skimage.morphology import remove_small_objects
from skimage.measure import label, regionprops

def process_image(input_image_path, output_image_path, labeled_image_path, min_size):
    try:
        # Read the image
        image = io.imread(input_image_path)
        
        # Ensure the image is binary
        binary_image = image > 0

        # Remove small objects
        filtered_image = remove_small_objects(binary_image, min_size=min_size)

        # Perform connected component labeling on the filtered image
        labeled_image = label(filtered_image)
        
        # Collect sizes of objects in the labeled image
        properties = regionprops(labeled_image)
        object_sizes = [{'filename': input_image_path, 'label': prop.label, 'size': prop.area} for prop in properties]

        
        # Convert images to unsigned 8-bit format for saving
        filtered_image_ubyte = img_as_ubyte(filtered_image)
        labeled_image_ubyte = img_as_ubyte(labeled_image)
        
        # Save the cleaned image
        io.imsave(output_image_path, img_as_ubyte(filtered_image))
        # Save the labeled image
        io.imsave(labeled_image_path, labeled_image_ubyte)

        print(f"Processed and saved filtered image at: {output_image_path}")
        print(f"Processed and saved labeled image at: {labeled_image_path}")
        
        return object_sizes

    except Exception as e:
        print(f"Error processing file {input_image_path}: {e}")
        return []

# # Replace with the path to your folder containing images
input_folder = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "outputs"
)   
min_size = 5000  # Minimum size of small objects to be removed, adjust as needed
csv_output_path = 'object_sizes.csv'  # Path to save the CSV file

all_object_sizes = []

# Process all images in the folder

for dirpath, dirnames, filenames in os.walk(input_folder):
    for filename in filenames:
        if filename.lower().endswith(("binary_mask.tif")):
            input_image_path = os.path.join(dirpath, filename)
            
            # Create a new filename to save the cleaned image
            name, ext = os.path.splitext(filename)
            filtered_filename = f"filtered_{name}{ext}"
            labeled_filename = f"label_{name}{ext}"
            filtered_file_path = os.path.join(dirpath, filtered_filename)
            labeled_file_path = os.path.join(dirpath, labeled_filename)
            
            object_sizes = process_image(input_image_path, filtered_file_path, labeled_file_path, min_size)
            all_object_sizes.extend(object_sizes)

    
    
    # Save object sizes to a CSV file
df = pd.DataFrame(all_object_sizes)
df.to_csv(csv_output_path, index=False)

print(f"Object sizes saved to {csv_output_path}")


# remove objects greater than 100k

import os
import pandas as pd
from skimage import io, img_as_ubyte
from skimage.morphology import remove_small_objects
from skimage.measure import label, regionprops

def process_image(input_image_path, cleaned_image_path, labeled_image_path, min_size, max_size):
    try:
        # Read the image
        image = io.imread(input_image_path)
        
        # Ensure the image is binary
        binary_image = image > 0

        # Remove small objects
        cleaned_image = remove_small_objects(binary_image, min_size=min_size)

        # Perform connected component labeling on the cleaned image
        labeled_image = label(cleaned_image)

        # Collect sizes of objects in the labeled image and remove large objects
        properties = regionprops(labeled_image)
        object_sizes = []
        for prop in properties:
            if prop.area <= max_size:
                object_sizes.append({'filename': input_image_path, 'label': prop.label, 'size': prop.area})
            else:
                # Set the pixels of large objects to 0 in the cleaned image
                cleaned_image[labeled_image == prop.label] = 0

        # Re-label the cleaned image after removing large objects
        labeled_image = label(cleaned_image)

        # Convert images to unsigned 8-bit format for saving
        cleaned_image_ubyte = img_as_ubyte(cleaned_image)
        labeled_image_ubyte = img_as_ubyte(labeled_image)

        # Save the cleaned image
        io.imsave(cleaned_image_path, cleaned_image_ubyte)

        # Save the labeled image
        io.imsave(labeled_image_path, labeled_image_ubyte)

        print(f"Processed and saved cleaned image at: {cleaned_image_path}")
        print(f"Processed and saved labeled image at: {labeled_image_path}")

        return object_sizes

    except Exception as e:
        print(f"Error processing file {input_image_path}: {e}")
        return []

# Example usage
input_folder = '/path/to/your/folder'  # Replace with the path to your folder containing images
min_size = 64  # Minimum size of small objects to be removed, adjust as needed
max_size = 100000  # Maximum size of objects to be retained
csv_output_path = 'object_sizes.csv'  # Path to save the CSV file

all_object_sizes = []

for dirpath, dirnames, filenames in os.walk(input_folder):
    for filename in filenames:
        if filename.lower().endswith((".tif", ".tiff")):
            input_image_path = os.path.join(dirpath, filename)
            
            # Create new filenames to save the cleaned and labeled images
            name, ext = os.path.splitext(filename)
            cleaned_filename = f"cleaned_{name}{ext}"
            labeled_filename = f"label_{name}{ext}"
            cleaned_file_path = os.path.join(dirpath, cleaned_filename)
            labeled_file_path = os.path.join(dirpath, labeled_filename)
            
            object_sizes = process_image(input_image_path, cleaned_file_path, labeled_file_path, min_size, max_size)
            all_object_sizes.extend(object_sizes)

# Save object sizes to a CSV file
df = pd.DataFrame(all_object_sizes)
df.to_csv(csv_output_path, index=False)

print(f"Object sizes saved to {csv_output_path}")
