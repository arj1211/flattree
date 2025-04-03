import os


def create_example_structure(base_dir):
    # Define the directories to be created
    directories = [
        os.path.join(base_dir, "subdir1"),
        os.path.join(base_dir, "subdir2", "nested"),
        os.path.join(base_dir, "logs"),
    ]
    
    # Create directories
    for d in directories:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Define files and their contents
    files = {
        os.path.join(base_dir, "subdir1", "file1.txt"): "This is file1 in subdir1.",
        os.path.join(base_dir, "subdir1", "file2.log"): "Log file in subdir1.",
        os.path.join(base_dir, "subdir2", "nested", "file3.py"): "print('Hello from file3')",
        os.path.join(base_dir, "subdir2", "nested", "file4.md"): "# File4 Markdown Content",
        os.path.join(base_dir, "file5.conf"): "config_value=123",
        os.path.join(base_dir, "file6.txt"): "Sample text file at the root level.",
        os.path.join(base_dir, "logs", "debug.log"): "Debug log content."
    }
    
    # Create files with the specified content
    for filepath, content in files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {filepath}")

if __name__ == "__main__":
    base_directory = os.path.join(os.getcwd(), "example_root")
    create_example_structure(base_directory)
    print(f"\nExample directory structure created at: {base_directory}")
