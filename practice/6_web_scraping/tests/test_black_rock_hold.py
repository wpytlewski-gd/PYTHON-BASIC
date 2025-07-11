from pathlib import Path

import black_rock_holds
import pytest
from bs4 import BeautifulSoup


# Fixture to provide mock HTML for the holders page
@pytest.fixture
def mock_holders_html():
    """Provides mock HTML content for the institutional holders page."""
    return """
    <section data-testid="holders-top-institutional-holders">
        <tbody>
            <tr>
                <td>Vanguard Group Inc</td>
                <td>10.5M</td>
                <td>Mar 30, 2023</td>
                <td>8.50%</td>
                <td>$7.5B</td>
            </tr>
            <tr>
                <td>SSgA Funds Management, Inc.</td>
                <td>5.2M</td>
                <td>Mar 30, 2023 </td>
                <td>4.20%</td>
                <td>$3.7B</td>
            </tr>
        </tbody>
    </section>
    """


def test_run_with_valid_html(tmp_path, mock_holders_html):
    """
    Tests the main `run` function with valid HTML to ensure it creates
    the output file with the correct holders data.
    """
    # Setup mock file system
    input_html_path = tmp_path / "blk_holders.html"
    input_html_path.write_text(mock_holders_html, encoding="utf-8")
    output_file = tmp_path / "blackrock_holders.txt"

    # Run the script
    black_rock_holds.run(output_path=output_file, input_html=input_html_path)

    # Assertions
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "10 largest holds of Blackrock Inc." in content
    assert "Vanguard Group Inc" in content
    assert "10.5M" in content
    assert "$7.5B" in content
    assert "SSgA Funds Management, Inc." in content


def test_run_with_malformed_html(tmp_path):
    """
    Tests that the script handles malformed or empty HTML gracefully
    without crashing.
    """
    input_html_path = tmp_path / "malformed.html"
    input_html_path.write_text("<div><p>No data here</p></div>", encoding="utf-8")
    output_file = tmp_path / "blackrock_holders.txt"

    # Run the script
    black_rock_holds.run(output_path=output_file, input_html=input_html_path)

    # The script should not create a file if no data is found
    assert not output_file.exists()


def test_run_with_empty_html(tmp_path):
    """
    Tests that the script handles an empty file without crashing.
    """
    input_html_path = tmp_path / "empty.html"
    input_html_path.touch()  # Creates an empty file
    output_file = tmp_path / "blackrock_holders.txt"

    # Run the script
    black_rock_holds.run(output_path=output_file, input_html=input_html_path)

    # The script should not create a file if the input is empty
    assert not output_file.exists()
