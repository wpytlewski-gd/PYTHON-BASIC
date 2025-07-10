import argparse
from pathlib import Path

from bs4 import BeautifulSoup
from utils import create_table_file, scrape_html


def run(output_path, input_html=None, base_link=None, table_title="10 largest holds of Blackrock Inc."):
    """Extracts top holders from an HTML file and saves them to a table."""
    if input_html:
        with open(input_html, encoding="utf-8") as f:
            main_soup = BeautifulSoup(f.read(), "html.parser")
    elif base_link is not None:
        main_soup = scrape_html(base_link + "/quote/BLK/holders/")

    holders_info = []

    try:
        top_holders_section = main_soup.find("section", attrs={"data-testid": "holders-top-institutional-holders"})
        top_holders_table_body = top_holders_section.find("tbody")

        for company_row in top_holders_table_body.find_all("tr")[:10]:
            cells = company_row.find_all("td")
            holders_info.append(
                {
                    "Name": cells[0].text.strip(),
                    "Shares": cells[1].text.strip(),
                    "Date Reported": cells[2].text.strip(),
                    "% Out": cells[3].text.strip(),
                    "Value": cells[4].text.strip(),
                }
            )
    except (AttributeError, IndexError):
        pass

    create_table_file(holders_info, table_title, output_path)


def main():
    """Parses arguments and executes the run function."""
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Find top institutional holders for a stock.")
    parser.add_argument("-i", "--input", default=str(script_dir / "pages"), help="Path to the source data directory.")
    parser.add_argument(
        "-o", "--output", default=str(script_dir / "blackrock_holders.txt"), help="Path to save the result file."
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    input_html = Path(args.input) / "blk_holders.html"
    # Run locally
    run(output_path, input_html)

    # Run with scraping
    # run(output_path, base_link="https://finance.yahoo.com")


if __name__ == "__main__":
    main()
