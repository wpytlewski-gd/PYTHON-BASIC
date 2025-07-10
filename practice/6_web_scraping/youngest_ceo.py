import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup
from utils import create_table_file, scrape_html


def get_ceo_name_and_year(soup: BeautifulSoup):
    """Gets the CEO's name and birth year from the profile page."""
    try:
        ceo_pattern = r"\b(CEO|Chief Executive Officer)\b"
        table_body = soup.find("table").find("tbody")
        for member in table_body.find_all("tr"):
            fields = member.find_all("td")
            title = fields[1].text.strip()
            if re.search(ceo_pattern, title, re.IGNORECASE):
                return fields[0].text.strip(), fields[-1].text.strip()
    except (AttributeError, IndexError):
        pass
    return "N/A", "N/A"


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


def get_company_country(soup: BeautifulSoup):
    """Gets the company's country from its profile."""
    try:
        company_info = soup.find("div", class_=re.compile("^company-info"))
        address_divs = company_info.find("div").find_all("div")
        return address_divs[-1].text.strip()
    except (AttributeError, IndexError):
        return "N/A"


def get_company_employees(soup: BeautifulSoup):
    """Gets the number of company employees."""
    try:
        company_stats = soup.find("dl", class_=re.compile("^company-stats"))
        employee_div = company_stats.find_all("div")[-1]
        return employee_div.find("dd").text.strip()
    except (AttributeError, IndexError):
        return "N/A"


def get_most_active_companies(soup: BeautifulSoup, get_link=False):
    """Gets the top 10 most active companies from the main table."""
    output_list = []
    try:
        table_body = soup.find("article").find("tbody")
        for row in table_body.find_all("tr")[:10]:
            cells = row.find_all("td")
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


def run(output_path, input_html=None, source_dir=None, base_link=None, table_title="5 stocks with youngest CEOs"):
    """Runs the main scraping and file generation process."""
    if input_html:
        with open(input_html, encoding="utf-8") as f:
            main_soup = BeautifulSoup(f.read(), "html.parser")
    elif base_link is not None:
        main_soup = scrape_html(base_link + "/markets/stocks/most-active/")

    most_active = get_most_active_companies(main_soup, get_link=(base_link is not None))

    companies_info = []
    for company in most_active:
        company_soup = None
        if source_dir:
            profile_file = Path(source_dir) / f"{company['code']}_profile.html"
            if profile_file.exists():
                with open(profile_file, encoding="utf-8") as f:
                    company_soup = BeautifulSoup(f.read(), "html.parser")
        elif base_link and company.get("link"):
            url = base_link + company["link"] + "/profile"
            company_soup = scrape_html(url)

        if company_soup:
            ceo_name, ceo_year_born = get_ceo_name_and_year(company_soup)
            companies_info.append(
                {
                    "Name": company["name"],
                    "Code": company["code"],
                    "Country": get_company_country(company_soup),
                    "Employees": get_company_employees(company_soup),
                    "CEO Name": ceo_name,
                    "CEO Year Born": ceo_year_born,
                }
            )

    sorted_data = sorted(companies_info, key=lambda c: c["CEO Year Born"], reverse=True)
    create_table_file(sorted_data[:5], table_title, output_path)


def main():
    """Parses arguments and executes the run function."""
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Find the 5 stocks with the youngest CEOs.")
    parser.add_argument("-i", "--input", default=str(script_dir / "pages"), help="Path to the source data directory.")
    parser.add_argument(
        "-o", "--output", default=str(script_dir / "most_youngest_ceo.txt"), help="Path to save the result file."
    )
    args = parser.parse_args()

    # Run locally
    run(
        output_path=Path(args.output),
        input_html=Path(args.input) / "main_page.html",
        source_dir=Path(args.input),
    )

    # Run with scraping
    # run(
    #     output_path=Path(args.output),
    #     base_link="https://finance.yahoo.com",
    # )


if __name__ == "__main__":
    main()
