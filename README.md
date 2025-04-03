# flattree
Small utility to flatten a directory into a `.txt` file and back again

1. **Copy Files**: Copy files from a source directory to a destination directory, preserving the directory structure. Optional regex filters allow including or excluding files.

2. **Concatenate Files**: Merge file contents (with file paths as headers) from a directory into a single text file.

3. **Reconstruct Files**: Rebuild the original files from the concatenated text file.

## usage

### copy files
```bash
python file_tool.py copy --root-dir /path/to/source --dest-dir /path/to/dest \
[--file-list file1 file2 ...] [--include "regex1" "regex2" ...] [--exclude "regex3" ...]
```
### concatenate files
```bash
python file_tool.py concatenate --source-dir /path/to/directory --output-file /path/to/output.txt
```
### reconstruct files
```bash
python file_tool.py reconstruct --input-file /path/to/output.txt --dest-dir /path/to/reconstructed
```

## automated testing

- `create_example_structure.py`: Creates a sample directory structure.
- `run_tests.sh`: Runs an automated test pipeline that creates a sample directory structure, copies, concatenates, and reconstructs files.
    - First run `chmod +x run_tests.sh` to make executable, then execute `run_tests.sh` script to test.