from pathlib import Path

import best_year_change
import pytest
from bs4 import BeautifulSoup


# Fixture to provide mock HTML for a company's statistics page
@pytest.fixture
def mock_stats_html():
    """Provides mock HTML content for a company's key-statistics page."""
    return """
    <article>
        <article>
            <div>
                <!-- Financials Section -->
                <section>
                    <div>
                        <!-- Balance Sheet Section -->
                        <section></section>
                        <section></section>
                        <section></section>
                        <section></section>
                        <section>
                            <table>
                                <tr><td>Total Cash</td><td>123.45B</td></tr>
                            </table>
                        </section>
                    </div>
                </section>
                <!-- Trading Information Section -->
                <section>
                    <div>
                        <!-- Stock Price History Section -->
                        <section>
                            <table>
                                <tr><td>Beta (5Y Monthly)</td><td>2.5</td></tr>
                                <tr><td>52-Week Change</td><td>+99.99%</td></tr>
                            </table>
                        </section>
                    </div>
                </section>
            </div>
        </article>
    </article>
    """


# Fixture to provide mock HTML for the best gainers page
@pytest.fixture
def mock_best_gainers_html():
    """Provides mock HTML content for the 52-week gainers page."""
    return """
    <article>
        <tbody>
            <tr>
                <td><a href="/quote/GME">GME</a></td>
                <td>GameStop Corp.</td>
            </tr>
        </tbody>
    </article>
    """


def test_get_total_cash(mock_stats_html):
    """
    Tests that the total cash is correctly extracted from the stats page.
    """
    soup = BeautifulSoup(mock_stats_html, "html.parser")
    total_cash = best_year_change.get_total_cash(soup)
    assert total_cash == "123.45B"


def test_get_year_change(mock_stats_html):
    """
    Tests that the 52-week change is correctly extracted from the stats page.
    """
    soup = BeautifulSoup(mock_stats_html, "html.parser")
    year_change = best_year_change.get_year_change(soup)
    assert year_change == "+99.99%"


def test_run_integration(tmp_path, mock_best_gainers_html, mock_stats_html):
    """
    Tests the main `run` function to ensure it creates the output file
    with the correctly processed data.
    """
    # Setup mock file system
    source_dir = tmp_path / "pages"
    source_dir.mkdir()
    output_file = tmp_path / "best_year_change.txt"
    main_page_file = source_dir / "best_year_change.html"
    main_page_file.write_text(mock_best_gainers_html, encoding="utf-8")

    # Create a mock stats file for one of the companies
    gme_stats_file = source_dir / "GME_stats.html"
    gme_stats_file.write_text(mock_stats_html, encoding="utf-8")

    # Run the script
    best_year_change.run(output_path=output_file, input_html=main_page_file, source_dir=source_dir)

    # Assertions
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "10 stocks with best 52-Week Change" in content
    assert "GameStop Corp." in content
    assert "GME" in content
    assert "+99.99%" in content
    assert "123.45B" in content
