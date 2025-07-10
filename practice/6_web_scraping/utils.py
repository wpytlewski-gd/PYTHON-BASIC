import requests
from bs4 import BeautifulSoup


def create_table_file(data, title, filename):
    # TODO: Simplify this?
    if not data:
        return

    headers = list(data[0].keys())

    col_widths = {h: len(h) for h in headers}
    for row in data:
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(row[h])))

    header_row = "| " + " | ".join([h.ljust(col_widths[h]) for h in headers]) + " |"
    separator = "-" * len(header_row)
    title_header = f" {title} ".center(len(header_row), "=")

    output = [title_header, header_row, separator]
    for row in data:
        data_row = "| " + " | ".join([str(row[h]).ljust(col_widths[h]) for h in headers]) + " |"
        output.append(data_row)

    with open(filename, "w") as f:
        f.write("\n".join(output))


def scrape_html(url):
    print("Scraping ...")
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")
