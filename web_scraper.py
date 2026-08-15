#!/usr/bin/env python3
"""
Web scraper que extrai citações do site quotes.toscrape.com e salva em SQLite.
Uso: python web_scraper.py [--pages N] [--db quotes.db]
"""
import argparse
import sqlite3
import sys
from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup


BASE_URL = "http://quotes.toscrape.com"


@dataclass
class Quote:
    text: str
    author: str
    tags: List[str]


def scrape_page(page: int) -> List[Quote]:
    url = f"{BASE_URL}/page/{page}/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    for div in soup.select("div.quote"):
        text = div.select_one("span.text").get_text(strip=True)
        author = div.select_one("small.author").get_text(strip=True)
        tags = [a.get_text(strip=True) for a in div.select("div.tags a.tag")]
        quotes.append(Quote(text=text, author=author, tags=tags))
    return quotes


def save_to_sqlite(quotes: List[Quote], db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                tags TEXT NOT NULL
            )
        """)
        for q in quotes:
            cursor.execute(
                "INSERT INTO quotes (text, author, tags) VALUES (?, ?, ?)",
                (q.text, q.author, ", ".join(q.tags))
            )
        conn.commit()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Scraper de citações para SQLite.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas a raspar")
    parser.add_argument("--db", type=str, default="quotes.db", help="Arquivo SQLite de saída")
    args = parser.parse_args()

    all_quotes: List[Quote] = []
    for page in range(1, args.pages + 1):
        try:
            print(f"Raspando página {page}...")
            quotes = scrape_page(page)
            if not quotes:
                print(f"Página {page} sem citações, parando.")
                break
            all_quotes.extend(quotes)
        except requests.RequestException as e:
            print(f"Erro na página {page}: {e}", file=sys.stderr)
            continue

    if all_quotes:
        save_to_sqlite(all_quotes, args.db)
        print(f"Salvas {len(all_quotes)} citações em {args.db}")
    else:
        print("Nenhuma citação coletada.", file=sys.stderr)


if __name__ == "__main__":
    main()