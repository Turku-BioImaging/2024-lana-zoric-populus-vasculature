import os
from skimage import io, transform
import numpy as np

SCALE_FACTOR = 0.5

def downsize_images_in_folder(input_folder):
    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for filename in filenames:
            # Construct the full file path
            file_path = os.path.join(dirpath, filename)

            # Check if the file is an image
            if filename.lower().endswith((".tif", ".tiff")):
                try:
                    # Read the image
                    image = io.imread(file_path)

                    # Print original image shape
                    print(f"Original image size: {image.shape}")

                    # Apply rescale with the given scale factor
                    # Using order=1 to ensure bilinear interpolation
                    resized_image = transform.rescale(
                        image,
                        scale_factor=SCALE_FACTOR,
                        anti_aliasing=True,
                        order=1,
                        channel_axis=-1,
                    )

                    # Clip the values to ensure they're in the correct range [0, 1] for float images
                    if resized_image.dtype == np.float64:
                        resized_image = np.clip(resized_image, 0, 1)

                    # Print resized image shape
                    print(f"Resized image size: {resized_image.shape}")

                    # Create a new filename to save the resized image
                    name, ext = os.path.splitext(filename)
                    resized_filename = f"rescale_{name}{ext}"
                    resized_file_path = os.path.join(dirpath, resized_filename)

                    # Save the resized image to the output path
                    io.imsave(resized_file_path, resized_image)

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


# Example usage
input_folder = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "outputs"
)  # Replace with the path to your folder containing images

downsize_images_in_folder(input_folder)
