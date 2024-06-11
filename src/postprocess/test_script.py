

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


# # remove objects greater than 100k

# import os
# import pandas as pd
# from skimage import io, img_as_ubyte
# from skimage.morphology import remove_small_objects
# from skimage.measure import label, regionprops

# def process_image(input_image_path, cleaned_image_path, labeled_image_path, min_size, max_size):
#     try:
#         # Read the image
#         image = io.imread(input_image_path)
        
#         # Ensure the image is binary
#         binary_image = image > 0

#         # Remove small objects
#         cleaned_image = remove_small_objects(binary_image, min_size=min_size)

#         # Perform connected component labeling on the cleaned image
#         labeled_image = label(cleaned_image)

#         # Collect sizes of objects in the labeled image and remove large objects
#         properties = regionprops(labeled_image)
#         object_sizes = []
#         for prop in properties:
#             if prop.area <= max_size:
#                 object_sizes.append({'filename': input_image_path, 'label': prop.label, 'size': prop.area})
#             else:
#                 # Set the pixels of large objects to 0 in the cleaned image
#                 cleaned_image[labeled_image == prop.label] = 0

#         # Re-label the cleaned image after removing large objects
#         labeled_image = label(cleaned_image)

#         # Convert images to unsigned 8-bit format for saving
#         cleaned_image_ubyte = img_as_ubyte(cleaned_image)
#         labeled_image_ubyte = img_as_ubyte(labeled_image)

#         # Save the cleaned image
#         io.imsave(cleaned_image_path, cleaned_image_ubyte)

#         # Save the labeled image
#         io.imsave(labeled_image_path, labeled_image_ubyte)

#         print(f"Processed and saved cleaned image at: {cleaned_image_path}")
#         print(f"Processed and saved labeled image at: {labeled_image_path}")

#         return object_sizes

#     except Exception as e:
#         print(f"Error processing file {input_image_path}: {e}")
#         return []

# # Example usage
# input_folder = '/path/to/your/folder'  # Replace with the path to your folder containing images
# min_size = 64  # Minimum size of small objects to be removed, adjust as needed
# max_size = 100000  # Maximum size of objects to be retained
# csv_output_path = 'object_sizes.csv'  # Path to save the CSV file

# all_object_sizes = []

# for dirpath, dirnames, filenames in os.walk(input_folder):
#     for filename in filenames:
#         if filename.lower().endswith((".tif", ".tiff")):
#             input_image_path = os.path.join(dirpath, filename)
            
#             # Create new filenames to save the cleaned and labeled images
#             name, ext = os.path.splitext(filename)
#             cleaned_filename = f"cleaned_{name}{ext}"
#             labeled_filename = f"label_{name}{ext}"
#             cleaned_file_path = os.path.join(dirpath, cleaned_filename)
#             labeled_file_path = os.path.join(dirpath, labeled_filename)
            
#             object_sizes = process_image(input_image_path, cleaned_file_path, labeled_file_path, min_size, max_size)
#             all_object_sizes.extend(object_sizes)

# # Save object sizes to a CSV file
# df = pd.DataFrame(all_object_sizes)
# df.to_csv(csv_output_path, index=False)

# print(f"Object sizes saved to {csv_output_path}")
