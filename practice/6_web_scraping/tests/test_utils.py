from pathlib import Path

import pytest
from utils import create_table_file


@pytest.fixture
def sample_data():
    """Provides a sample list of dictionaries for table creation."""
    return [
        {"Name": "Test Inc.", "Code": "TEST", "Value": 100},
        {"Name": "Another Co", "Code": "AC", "Value": 12345},
    ]


def test_create_table_file_generation(tmp_path, sample_data):
    """
    Tests if the table file is created with the correct title, headers,
    and data, including proper alignment and spacing.
    """
    output_file = tmp_path / "test_table.txt"
    title = "Sample Test Table"

    create_table_file(sample_data, title, output_file)

    assert output_file.exists()
    content = output_file.read_text().splitlines()

    # Check title
    assert title in content[0]
    assert content[0].strip("=") == f" {title} "

    # Check header
    assert "| Name       | Code | Value |" in content[1]

    # Check separator
    assert "-----------" in content[2]

    # Check data rows
    assert "| Test Inc.  | TEST | 100   |" in content[3]
    assert "| Another Co | AC   | 12345 |" in content[4]


def test_create_table_file_empty_data(tmp_path):
    """
    Tests that no file is created when the input data is empty,
    as per the function's logic.
    """
    output_file = tmp_path / "empty_table.txt"
    create_table_file([], "Empty Table", output_file)
    assert not output_file.exists()


def test_column_width_calculation(tmp_path, sample_data):
    """
    Tests that column widths are calculated correctly based on the longest
    item in each column (including the header).
    """
    output_file = tmp_path / "width_test.txt"
    create_table_file(sample_data, "Width Test", output_file)

    content = output_file.read_text().splitlines()
    header_row = content[1]
    data_row_1 = content[3]

    # 'Another Co' is 10 chars, 'Name' is 4. Width should be 10.
    # 'Value' is 5, '12345' is 5. Width should be 5.
    expected_header = "| Name       | Code | Value |"
    expected_data_1 = "| Test Inc.  | TEST | 100   |"

    # Adjusting for the sample data provided in the fixture
    # Name: max(len('Name'), len('Test Inc.'), len('Another Co')) = 10
    # Code: max(len('Code'), len('TEST'), len('AC')) = 4
    # Value: max(len('Value'), len('100'), len('12345')) = 5
    expected_header = "| Name       | Code | Value |"
    expected_data_1 = "| Test Inc.  | TEST | 100   |"
    expected_data_2 = "| Another Co | AC   | 12345 |"

    assert header_row.startswith("| Name      ")
    assert "| Code " in header_row
    assert "| Value " in header_row
    assert data_row_1.startswith("| Test Inc. ")
