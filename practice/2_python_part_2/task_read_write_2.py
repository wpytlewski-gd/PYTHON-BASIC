"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""

import os


def generate_words(n=20):
    import random
    import string

    words = list()
    for _ in range(n):
        word = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def main(output_dir):
    words_list = generate_words()

    output_path = os.path.join(output_dir, "results_utf8.txt")
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(words_list))

    output_path = os.path.join(output_dir, "results_cp1252.txt")
    with open(output_path, "w", encoding="cp1252") as file_handle:
        file_handle.write(",".join(reversed(words_list)))


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    files_dir = os.path.join(script_dir, "files")
    main(files_dir)
