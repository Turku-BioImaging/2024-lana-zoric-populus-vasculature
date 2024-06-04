

// Prompt to select the parent directory
dir = getDirectory("Select parent directory");

//if (dir == null)
//    exit("User canceled the dialog");

// Prompt to select a subdirectory
subdir = getDirectory("Select subdirectory within " + dir);

//if (subdir == null)
//    exit("User canceled the dialog");

// Get list of TIFF files in the selected subdirectory
list = getFileList(subdir);

// Create output directory for processed images
outputDir = subdir + "processed_images" + File.separator;
File.makeDirectory(outputDir);

// Process each TIFF file
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif") || endsWith(list[i], ".tiff")) {
        // Open the image
        open(subdir + list[i]);
        name = getTitle();
        
        // process the image
        run("Scale...", "x=0.5 y=0.5 width=2000 height=1500 interpolation=Bilinear average create");
        
        // Save the process image
        saveAs("Tiff", outputDir + "processed_" + name);
        
        // Close the original image
        close("*");
    }
}

// Alert user about completion
print("Processing complete. Processed images saved in " + outputDir);
