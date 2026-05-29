import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os
import time

PAGES = {
    "mazda": "https://en.wikipedia.org/wiki/Mazda",
    "mazda3": "https://en.wikipedia.org/wiki/Mazda3",
    "mazda6": "https://en.wikipedia.org/wiki/Mazda6",
    "mx5": "https://en.wikipedia.org/wiki/Mazda_MX-5",
    "rx7": "https://en.wikipedia.org/wiki/Mazda_RX-7",
    "rx8": "https://en.wikipedia.org/wiki/Mazda_RX-8",
    "cx5": "https://en.wikipedia.org/wiki/Mazda_CX-5",
    "cx50": "https://en.wikipedia.org/wiki/Mazda_CX-50",
    "cx90": "https://en.wikipedia.org/wiki/Mazda_CX-90",
    "skyactiv": "https://en.wikipedia.org/wiki/SkyActiv",
    "wankel": "https://en.wikipedia.org/wiki/Wankel_engine"
}

def clean_text(content):
    for tag in content.find_all(["table", "sup", "style", "script", "img"]):
        tag.decompose()
    return content.get_text(separator="\n").strip()

def scrape_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    content = soup.find("div", class_="mw-parser-output")
    if content is None:
        raise ValueError("Could not find main content on page: " + url)

    return clean_text(content)

def save_as_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Unicode font (no "uni=True" needed in fpdf2)
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf")
    pdf.set_font("DejaVu", size=11)

    for line in text.split("\n"):
        pdf.multi_cell(0, 6, line)

    pdf.output(f"data/raw/{filename}.pdf")

def main():
    os.makedirs("data/raw", exist_ok=True)

    for name, url in PAGES.items():
        print(f"Scraping {name}...")
        text = scrape_page(url)
        save_as_pdf(text, name)
        time.sleep(1)

if __name__ == "__main__":
    main()
