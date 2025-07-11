from pathlib import Path

import pytest
import youngest_ceo
from bs4 import BeautifulSoup


# Fixture to provide mock HTML for a company's profile page
@pytest.fixture
def mock_profile_html():
    """Provides a mock HTML content for a company profile page."""
    return """
    <article>
        <h1>Tesla, Inc. (TSLA)</h1>
        <div class="company-info">
            <div>
                <div>123 Electric Drive</div>
                <div>Palo Alto, CA 94304</div>
                <div>United States</div>
            </div>
        </div>
        <dl class="company-stats">
            <div><dt>Sector</dt><dd>Automotive</dd></div>
            <div><dt>Employees</dt><dd>99290</dd></div>
        </dl>
        <table>
            <tbody>
                <tr>
                    <td>Mr. Zachary J. Kirkhorn</td>
                    <td>Master of Coin</td>
                    <td>-</td>
                    <td>-</td>
                    <td>1985</td>
                </tr>
                <tr>
                    <td>Mr. Elon R. Musk</td>
                    <td>Technoking of Tesla, CEO & Director</td>
                    <td>-</td>
                    <td>-</td>
                    <td>1971</td>
                </tr>
            </tbody>
        </table>
    </article>
    """


# Fixture to provide mock HTML for the main "most-active" page
@pytest.fixture
def mock_main_page_html():
    """Provides a mock HTML content for the most-active stocks page."""
    return """
    <article>
        <tbody>
            <tr>
                <td><a href="/quote/TSLA">TSLA</a></td>
                <td>Tesla, Inc.</td>
            </tr>
            <tr>
                <td><a href="/quote/AAPL">AAPL</a></td>
                <td>Apple Inc.</td>
            </tr>
        </tbody>
    </article>
    """


def test_get_ceo_name_and_year(mock_profile_html):
    """
    Tests the get_ceo_name_and_year function to ensure it correctly
    extracts the CEO's name and birth year from the HTML.
    """
    soup = BeautifulSoup(mock_profile_html, "html.parser")
    name, year = youngest_ceo.get_ceo_name_and_year(soup)
    assert name == "Mr. Elon R. Musk"
    assert year == "1971"


def test_get_company_details(mock_profile_html):
    """
    Tests other data extraction functions like country and employee count.
    """
    soup = BeautifulSoup(mock_profile_html, "html.parser")
    country = youngest_ceo.get_company_country(soup)
    employees = youngest_ceo.get_company_employees(soup)
    assert country == "United States"
    assert employees == "99290"


def test_run_integration(tmp_path, mock_main_page_html, mock_profile_html):
    """
    Tests the main `run` function to ensure it creates the output file
    with the correctly processed and sorted data.
    """
    # Setup mock file system
    source_dir = tmp_path / "pages"
    source_dir.mkdir()
    output_file = tmp_path / "youngest_ceo.txt"
    main_page_file = source_dir / "main_page.html"
    main_page_file.write_text(mock_main_page_html, encoding="utf-8")

    # Create a mock profile file for one of the companies
    tsla_profile = source_dir / "TSLA_profile.html"
    tsla_profile.write_text(mock_profile_html, encoding="utf-8")

    # Run the script
    youngest_ceo.run(output_path=output_file, input_html=main_page_file, source_dir=source_dir)

    # Assertions
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "5 stocks with youngest CEOs" in content
    assert "Mr. Elon R. Musk" in content
    assert "1971" in content
    assert "TSLA" in content
