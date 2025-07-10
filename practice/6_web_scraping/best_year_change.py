import argparse
from pathlib import Path

from bs4 import BeautifulSoup
from utils import create_table_file, scrape_html


def get_total_cash(soup: BeautifulSoup):
    """Gets total comapny cash."""
    try:
        financial_section = soup.find("article").find("article").find("div").find_all("section", recursive=False)[0]
        balance_section = financial_section.find("div").find_all("section", recursive=False)[4]
        total_cash_row = balance_section.find("table").find_all("tr")[0]
        total_cash = total_cash_row.find_all("td")[1]
        return total_cash.text.strip()
    except (AttributeError, IndexError):
        return "N/A"


def get_year_change(soup: BeautifulSoup):
    """Gets the 52-week change value."""
    try:
        trading_info_section = soup.find("article").find("article").find("div").find_all("section", recursive=False)[1]
        stoc_price_history = trading_info_section.find("div").find_all("section", recursive=False)[0]
        year_change_row = stoc_price_history.find("table").find_all("tr")[1]
        year_change = year_change_row.find_all("td")[1]
        return year_change.text.strip()
    except (AttributeError, IndexError):
        return "N/A"


def get_company_name_and_code(soup: BeautifulSoup):
    """Gets company name and code."""
    try:
        title_tag = soup.find("article").find("h1")
        split_title = title_tag.text.rsplit("(", 1)
        name = split_title[0].strip()
        code = split_title[1].rstrip(")").strip()
        return name, code
    except (AttributeError, IndexError):
        return "N/A", "N/A"


def get_best_gainers(soup: BeautifulSoup, get_link=False):
    """Gets the best gainers from the main table."""
    output_list = []
    try:
        best_gainers_table = soup.find("article").find("tbody")
        for company_row in best_gainers_table.find_all("tr")[:10]:
            cells = company_row.find_all("td")
            company_info = {
                "code": cells[0].text.strip(),
                "name": cells[1].text.strip(),
            }
            if get_link:
                link_tag = cells[0].find("a")
                company_info["link"] = link_tag["href"] if link_tag else ""
            output_list.append(company_info)
    except (AttributeError, IndexError, KeyError):
        return []
    return output_list


def run(
    output_path, input_html=None, source_dir=None, base_link=None, table_title="10 stocks with best 52-Week Change"
):
    """Runs the main scraping and file generation process."""
    if input_html:
        with open(input_html, encoding="utf-8") as f:
            main_soup = BeautifulSoup(f.read(), "html.parser")
    elif base_link is not None:
        main_soup = scrape_html(base_link + "/markets/stocks/52-week-gainers/")

    best_gainers = get_best_gainers(main_soup, get_link=(base_link is not None))

    companies_info = []
    for company in best_gainers:
        company_soup = None
        if source_dir:
            stats_file = Path(source_dir) / f"{company['code']}_stats.html"
            if stats_file.exists():
                with open(stats_file, encoding="utf-8") as f:
                    company_soup = BeautifulSoup(f.read(), "html.parser")
        elif base_link and company.get("link"):
            url = base_link + company["link"] + "/key-statistics/"
            company_soup = scrape_html(url)

        if company_soup:
            companies_info.append(
                {
                    "Name": company["name"],
                    "Code": company["code"],
                    "52-Week Change": get_year_change(company_soup),
                    "Total Cash": get_total_cash(company_soup),
                }
            )

    create_table_file(companies_info, table_title, output_path)


def main():
    """Parses arguments and executes the run function."""
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Find stocks with the best 52-week change.")
    parser.add_argument("-i", "--input", default=str(script_dir / "pages"), help="Path to the source data directory.")
    parser.add_argument(
        "-o", "--output", default=str(script_dir / "best_year_change.txt"), help="Path to save the result file."
    )
    args = parser.parse_args()

    # Run locally
    run(
        output_path=Path(args.output),
        input_html=Path(args.input) / "best_year_change.html",
        source_dir=Path(args.input),
    )

    # Run with scraping
    # run(
    #     output_path=Path(args.output),
    #     base_link="https://finance.yahoo.com",
    # )


if __name__ == "__main__":
    main()
