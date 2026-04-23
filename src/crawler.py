import requests
import json
import os
from warcio.archiveiterator import ArchiveIterator

BASE_URL = "https://data.commoncrawl.org/"
WET_PATH = "crawl-data/CC-MAIN-2026-08/segments/1770395505396.36/wet/CC-MAIN-20260206181458-20260206211458-00000.warc.wet.gz"
FULL_URL = BASE_URL + WET_PATH

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_record(uri: str, text: str, raw_file):
    """Save a single WET record as a JSON line (JSONL format)."""
    record = {"uri": uri, "text": text.strip()}
    raw_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def extract_tech_data(url: str, limit: int = None):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    count = 0
    output_path = os.path.join(OUTPUT_DIR, "raw.jsonl")

    with open(output_path, "a", encoding="utf-8") as raw_file:
        for record in ArchiveIterator(response.raw):
            if record.rec_type != "conversion":
                continue

            lang = record.rec_headers.get_header("WARC-Identified-Content-Language")
            
            # If present and doesn't contain ENGLISH then reject the document.
            if lang and "eng" not in lang:
                continue
            
            uri = record.rec_headers.get_header("WARC-Target-URI")
            text = record.content_stream().read().decode("utf-8", errors="ignore")

            if not text.strip():
                continue

            save_record(uri, text, raw_file)
            count += 1

            if count % 100 == 0:
                print(f"[{count}] Last URI: {uri}")

            if limit and count >= limit:
                print(f"Reached limit of {limit} records.")
                break

    print(f"Done. {count} records saved to {output_path}")


extract_tech_data(FULL_URL, limit=2000)