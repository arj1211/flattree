#!/bin/bash
# run_tests.sh - Automated testing script for file processing tool

# Exit immediately if a command exits with a non-zero status.
set -e

# Define folder names for testing.
COPY_DIRNAME="copy_dest"

# Define paths for testing.
EXAMPLE_DIR="./example_root"
COPY_DEST="./$COPY_DIRNAME"
CONCATENATED_FILE="./concatenated.txt"
RECONSTRUCT_DIR="./reconstructed"

# Clean up previous test artifacts.
echo "Cleaning up previous test directories/files..."
rm -rf "$EXAMPLE_DIR" "$COPY_DEST" "$RECONSTRUCT_DIR" "$CONCATENATED_FILE"


# Step 1: Create the example directory structure.
echo "Creating example directory structure..."
python create_example_structure.py


# Step 2: Use the copy command.
# Example: Copy only text and Python files, and exclude any files that match 'debug.log'
echo "Copying files from example directory to copy destination..."
python file_tool.py copy \
    --root-dir "$EXAMPLE_DIR" \
    --dest-dir "$COPY_DEST" \
    --include ".*\.txt" ".*\.py" \
    --exclude "debug\.log"


# Step 3: Concatenate the copied files.
echo "Concatenating files into a single output file..."
python file_tool.py concatenate \
    --source-dir "$COPY_DEST" \
    --output-file "$CONCATENATED_FILE"



# Step 4: Reconstruct files from the concatenated output.
echo "Reconstructing files from concatenated file..."
python file_tool.py reconstruct \
    --input-file "$CONCATENATED_FILE" \
    --dest-dir "$RECONSTRUCT_DIR"


# Step 5: Compare the original and reconstructed directories.
echo "Comparing original and reconstructed directories..."
diff -r "$COPY_DEST" "$RECONSTRUCT_DIR/$COPY_DIRNAME" && echo "Directories match!" || echo "Differences found!"

# Clean up test artifacts.
echo "Cleaning up test directories/files..."
rm -rf "$EXAMPLE_DIR" "$COPY_DEST" "$RECONSTRUCT_DIR" "$CONCATENATED_FILE"

echo "Automated testing complete."
