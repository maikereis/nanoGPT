import requests
from config import BOOK_URL, RAW_DATA_FILEPATH, CORPUSE_DATA_FILEPATH
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

import sys




def download_data():
    response = requests.get(BOOK_URL)
    with open(RAW_DATA_FILEPATH, "wb") as file:
        file.write(response.content)
    print("File downloaded successfully!")


# Code adapted from Zaza Zakarias's article: Turn your EBook to Text with Python In seconds
# URL: https://medium.com/@zazazakaria18/turn-your-ebook-to-text-with-python-in-seconds-2a1e42804913, Accessed in 09/22/2024.

blacklist = [
    "[document]",
    "noscript",
    "header",
    "html",
    "meta",
    "head",
    "input",
    "script",
]

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path, {"ignore_ncx": True})
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def chap2text(chap):
    output = []
    soup = BeautifulSoup(chap, "html.parser")
    text = soup.find_all(string=True)  # Updated to 'string=True'
    for t in text:
        if t.parent.name not in blacklist:
            output.append(t)
    return " ".join(output)


def thtml2ttext(thtml):
    return [chap2text(html) for html in thtml]


def epub2text(epub_path):
    try:
        chapters = epub2thtml(epub_path)
        return thtml2ttext(chapters)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def convert():
    book_lines = epub2text(RAW_DATA_FILEPATH)

    with open(CORPUSE_DATA_FILEPATH, "a") as file:
        file.writelines(book_lines)

    print("File conversion successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a function to run: 'download' or 'convert'")
    else:
        if sys.argv[1] == "download":
            download_data()
        elif sys.argv[1] == "convert":
            convert()
        else:
            print("Unknown command. Use 'download' or 'convert'.")
