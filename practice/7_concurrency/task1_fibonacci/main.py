import csv
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from random import randint

# --- Configuration ---
MAX_FIB_INDEX = 20
MIN_FIB_INDEX = 0
NUMBER_OF_FILES = 10

# --- File Paths ---
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
RESULT_FILE = SCRIPT_DIR / "output/result.csv"


def fib(n: int):
    """Calculates a value in the Fibonacci sequence by its ordinal number."""
    f0, f1 = 0, 1
    for _ in range(n):
        f0, f1 = f1, f0 + f1
    return f0


def write_fib(fib_idx: int):
    """Calculates a single Fibonacci number and writes it to a file, returning a status string."""
    sys.set_int_max_str_digits(0)
    try:
        value = fib(fib_idx)
        value_str = str(value)
        filepath = OUTPUT_DIR / f"{fib_idx}.txt"
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.write(value_str)
        return f"Success: {fib_idx}"

    except Exception as e:
        return f"Failed to process index {fib_idx}: {e}"


def func1(array: list):
    """Runs write_fib for each number in the array using multiple processes and prints failures."""
    with ProcessPoolExecutor() as executor:
        results = executor.map(write_fib, array)

        for result in results:
            if result.startswith("Failed"):
                print(result)
    return


def read_and_parse_file(filepath: Path):
    """Reads a file's content and returns its name (as index) and content."""
    try:
        content = filepath.read_text(encoding="utf-8").strip()
        return (filepath.stem, content)
    except Exception as e:
        return (f"Failed: {filepath.name}", str(e))


def func2(source_dir: Path, result_file: Path):
    """Reads all txt files from a directory concurrently and writes them to a single CSV file."""
    files_to_process = list(source_dir.glob("*.txt"))
    all_data = []

    with ThreadPoolExecutor() as executor:
        results = executor.map(read_and_parse_file, files_to_process)
        for result in results:
            if isinstance(result[0], str) and result[0].startswith("Failed"):
                print(f"Error processing file: {result[0]} -> {result[1]}")
            else:
                all_data.append(result)

    try:
        with open(result_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(all_data)
    except Exception as e:
        print(f"Failed to write CSV file: {e}")
    return


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # TASK 1
    fib_indices = [randint(MIN_FIB_INDEX, MAX_FIB_INDEX) for _ in range(NUMBER_OF_FILES)]  # noqa: S311
    print(f"Processing {len(fib_indices)} files...")

    start_time = time.perf_counter()
    func1(array=fib_indices)
    duration = time.perf_counter() - start_time

    print(f"\nFinished in {duration:.2f} seconds.")

    # TASK 2
    print("\nAggregating results into a single CSV file...")
    start_time = time.perf_counter()
    func2(source_dir=OUTPUT_DIR, result_file=RESULT_FILE)
    duration = time.perf_counter() - start_time
    print(f"Task 2 (aggregation) finished in {duration:.2f} seconds.")
