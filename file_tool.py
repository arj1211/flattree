import argparse
import os
import re
import shutil

SEPARATOR = "~=" * 25


def file_matches(
    filename, file_list=None, include_patterns=None, exclude_patterns=None
):
    """Determine if a file should be processed based on the filters."""
    # Check explicit file list if provided.
    if file_list and filename not in file_list:
        return False
    # Check include patterns if provided.
    if include_patterns:
        if not any(re.search(pattern, filename) for pattern in include_patterns):
            return False
    # Check exclude patterns if provided.
    if exclude_patterns:
        if any(re.search(pattern, filename) for pattern in exclude_patterns):
            return False
    return True


def copy_files_with_structure(
    root_dir, dest_dir, file_list=None, include_patterns=None, exclude_patterns=None
):
    """
    Walk through root_dir, and copy files that satisfy the filtering conditions to dest_dir,
    preserving the directory structure.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if file_matches(filename, file_list, include_patterns, exclude_patterns):
                # Construct the full file path.
                file_path = os.path.join(dirpath, filename)
                # Compute the relative path and the destination directory.
                relative_path = os.path.relpath(dirpath, root_dir)
                target_dir = os.path.join(dest_dir, relative_path)
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(file_path, target_dir)
                print(f"Copied: {file_path} -> {target_dir}")


def concatenate_files_with_paths(source_dir, output_file):
    """
    Walk through source_dir and write each file's path and content into output_file.
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        for dirpath, _, filenames in os.walk(source_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                outfile.write(f"{SEPARATOR}\nfile: {file_path}\n~~~~~~~~~~\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Error reading file: {e}]")
                outfile.write(f"\n{SEPARATOR}\n")
                print(f"Appended: {file_path}")


def reconstruct_files_from_txt(input_file, dest_dir):
    """
    Reconstruct original files from a concatenated text file.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        content = infile.read()

    sections = content.split(SEPARATOR)
    for section in sections:
        if section.strip():
            lines = section.strip().split("\n")
            if len(lines) < 3:
                continue
            # The first line should contain the file path.
            file_path_line = lines[0].strip()
            if not file_path_line.startswith("file: "):
                continue
            original_file_path = file_path_line.replace("file: ", "", 1)
            file_content = "\n".join(lines[2:])
            # Reconstruct destination path.
            # Here we assume the file_path is absolute; we make it relative by stripping leading separators.
            relative_path = os.path.relpath(
                original_file_path, os.path.commonprefix([original_file_path, dest_dir])
            )
            dest_file_path = os.path.join(dest_dir, relative_path)
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            with open(dest_file_path, "w", encoding="utf-8") as outfile:
                outfile.write(file_content)
            print(f"Reconstructed: {dest_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="File processing tool to copy, concatenate, and reconstruct files."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Sub-command to run"
    )

    # Subparser for copy command.
    copy_parser = subparsers.add_parser(
        "copy", help="Copy files while preserving directory structure."
    )
    copy_parser.add_argument(
        "--root-dir", required=True, help="Source root directory to search files."
    )
    copy_parser.add_argument(
        "--dest-dir", required=True, help="Destination directory to copy files into."
    )
    copy_parser.add_argument(
        "--file-list", nargs="*", help="List of file names to copy (exact match)."
    )
    copy_parser.add_argument(
        "--include", nargs="*", help="Regex patterns; file must match at least one."
    )
    copy_parser.add_argument(
        "--exclude",
        nargs="*",
        help="Regex patterns; file matching any will be skipped.",
    )

    # Subparser for concatenate command.
    concat_parser = subparsers.add_parser(
        "concatenate", help="Concatenate file contents with paths into one text file."
    )
    concat_parser.add_argument(
        "--source-dir", required=True, help="Source directory to read files from."
    )
    concat_parser.add_argument(
        "--output-file",
        required=True,
        help="Output text file to write concatenated data.",
    )

    # Subparser for reconstruct command.
    recon_parser = subparsers.add_parser(
        "reconstruct", help="Reconstruct files from a concatenated text file."
    )
    recon_parser.add_argument(
        "--input-file", required=True, help="Input concatenated text file."
    )
    recon_parser.add_argument(
        "--dest-dir",
        required=True,
        help="Destination directory to reconstruct files into.",
    )

    args = parser.parse_args()

    if args.command == "copy":
        copy_files_with_structure(
            root_dir=args.root_dir,
            dest_dir=args.dest_dir,
            file_list=args.file_list,
            include_patterns=args.include,
            exclude_patterns=args.exclude,
        )
    elif args.command == "concatenate":
        concatenate_files_with_paths(
            source_dir=args.source_dir, output_file=args.output_file
        )
    elif args.command == "reconstruct":
        reconstruct_files_from_txt(input_file=args.input_file, dest_dir=args.dest_dir)


if __name__ == "__main__":
    main()
