"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os


def process_files(files_dir: str, num_of_files: int = 20) -> None:
    values = []
    for i in range(1, num_of_files + 1):
        file_path = os.path.join(files_dir, f"file_{i}.txt")

        with open(file_path, "r") as file_handle:
            content = file_handle.read().strip()
            if content:
                values.append(content)

    output_path = f"{files_dir}/result.txt"

    with open(output_path, "w") as file_handle:
        file_handle.write(", ".join(values))


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    files_dir = os.path.join(script_dir, "files")
    process_files(files_dir, 20)
