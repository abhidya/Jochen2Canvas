"""Offline Jochen class-diary parser for the archived Canvas sync project."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


@dataclass(frozen=True)
class DiaryItem:
    due_date: str
    title: str


class BodyTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[str] = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.items.append(text)


def parse_diary(html: str, year: int = 2018) -> list[DiaryItem]:
    parser = BodyTextParser()
    parser.feed(html)
    results: list[DiaryItem] = []
    current_day = ""

    for text in parser.items:
        if re.match(r"^[A-Z][a-z]{2} [A-Z][a-z]{2} \d{1,2}:?$", text):
            current_day = text.rstrip(":")
            continue
        if current_day:
            due_date = dt.datetime.strptime(f"{current_day} {year}", "%a %b %d %Y").strftime("%Y-%m-%d")
            results.append(DiaryItem(due_date=due_date, title=text))
            current_day = ""

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Jochen class diary HTML without Canvas credentials.")
    parser.add_argument("--fixture", type=Path, default=Path("fixtures/jochen_diary.html"))
    parser.add_argument("--year", type=int, default=2018)
    parser.add_argument("--live", action="store_true", help="Always refused in this archive.")
    args = parser.parse_args()

    if args.live:
        raise SystemExit("Live Canvas sync is disabled in this archive. Use the offline parser fixture.")

    items = parse_diary(args.fixture.read_text(encoding="utf-8"), year=args.year)
    for item in items:
        print(f"{item.due_date}: {item.title}")
    print(f"parsed_items={len(items)} network_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
