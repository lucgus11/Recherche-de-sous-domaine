#!/usr/bin/env python3
"""Google Sites subpage finder.

Example:
  python search_subpages.py \
    --base "https://sites.google.be/indse/be/geographie" \
    --words wordlist.txt
"""

import argparse
import concurrent.futures
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

DEFAULT_TIMEOUT = 10


def read_wordlist(path: Path) -> list[str]:
    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.strip()
        if word and not word.startswith("#"):
            words.append(word)
    return words


def check_url(session: requests.Session, url: str, timeout: int) -> tuple[str, bool, int]:
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True)
        return url, response.status_code < 400, response.status_code
    except requests.RequestException:
        return url, False, 0


def find_subpages(base_url: str, words: list[str], workers: int, timeout: int) -> list[tuple[str, int]]:
    base = base_url.rstrip("/") + "/"
    results: list[tuple[str, int]] = []
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(check_url, session, urljoin(base, word), timeout)
                for word in words
            ]
            for future in concurrent.futures.as_completed(futures):
                url, ok, status = future.result()
                if ok:
                    results.append((url, status))
    return sorted(results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find existing Google Sites subpages using a wordlist."
    )
    parser.add_argument("--base", required=True, help="Base URL of the Google Site")
    parser.add_argument("--words", required=True, help="Path to wordlist file")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers")
    parser.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT, help="Request timeout in seconds"
    )
    parser.add_argument(
        "--output",
        help="Optional output file to save found URLs (one per line)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    wordlist_path = Path(args.words)
    words = read_wordlist(wordlist_path)
    start = time.time()
    matches = find_subpages(args.base, words, args.workers, args.timeout)
    duration = time.time() - start

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(
            "\n".join(url for url, _ in matches), encoding="utf-8"
        )

    print("Found subpages:")
    for url, status in matches:
        print(f"- {url} (HTTP {status})")
    print(f"Checked {len(words)} candidates in {duration:.2f}s")


if __name__ == "__main__":
    main()
