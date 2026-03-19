import argparse
import csv
import logging
import time
from pathlib import Path
from typing import Iterator
from urllib.parse import urlsplit, urlunsplit

import requests
from requests.adapters import HTTPAdapter, Retry

from client import AIClient, MODEL_NAME
from prompts.bill_enrichment import EnrichedBill, prompt as bill_enrichment_prompt

logger = logging.getLogger(__name__)
DEFAULT_CONNECT_TIMEOUT_SECONDS = 10
DEFAULT_READ_TIMEOUT_SECONDS = 60
REQUEST_TIMEOUT = (DEFAULT_CONNECT_TIMEOUT_SECONDS, DEFAULT_READ_TIMEOUT_SECONDS)

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=None,
    raise_on_redirect=True,
    raise_on_status=True,
)
session = requests.Session()
session.headers.update(
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"}
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)


def fetch_pdf(pdf_url: str) -> bytes | None:
    normalized_url = strip_url_fragment(pdf_url)
    started_at = time.monotonic()
    try:
        response = session.get(normalized_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.Timeout:
        elapsed = time.monotonic() - started_at
        logger.error(
            "Timed out fetching PDF after %.2fs: %s (connect=%ss, read=%ss)",
            elapsed,
            normalized_url,
            DEFAULT_CONNECT_TIMEOUT_SECONDS,
            DEFAULT_READ_TIMEOUT_SECONDS,
        )
        return None
    except requests.RequestException as exc:
        elapsed = time.monotonic() - started_at
        logger.error("Failed to fetch PDF after %.2fs: %s (%s)", elapsed, normalized_url, exc)
        return None

    elapsed = time.monotonic() - started_at
    logger.info(
        "Fetched PDF in %.2fs: %s (%s bytes)",
        elapsed,
        normalized_url,
        len(response.content),
    )
    return response.content


def strip_url_fragment(url: str) -> str:
    split_url = urlsplit(url)
    return urlunsplit(split_url._replace(fragment=""))


def run_bill_enrichment(
    input_data_start_idx: int = 0,
    input_data_end_idx: int | None = None,
    sleep_between_calls: int = 30,
):
    """
    Run bill enrichment over a slice of the input CSV.

    input_data_end_idx may be None to indicate 'to the end'.
    """
    input_file_name = "bills_before_parliament_for_enrichment.csv"

    client = AIClient()
    with open(f"static_data/{input_file_name}", mode='r') as file:
        csv_dict: Iterator[dict[str, str]] = csv.DictReader(file)
        rows = list(csv_dict)
        slice_rows = rows[input_data_start_idx:input_data_end_idx]
        for idx, row in enumerate(slice_rows):
            bill_title = row["title"]
            explanatory_memo_pdf_url=row["explanatory_memo_pdf_url"]
            bill_digest_pdf_url=row["bill_digest_pdf_url"]
            logger.info("Processing bill '%s'", bill_title)
            logger.debug("Explanatory memo PDF URL: %s", explanatory_memo_pdf_url)
            logger.debug("Bill digest PDF URL: %s", bill_digest_pdf_url)
            memo_pdf = fetch_pdf(explanatory_memo_pdf_url)
            if memo_pdf is None:
                logger.error("Failed to fetch explanatory memo for bill '%s'", bill_title)
                continue
            logger.info("Fetched explanatory memo for bill '%s'", bill_title)
            pdfs = [memo_pdf]
            if bill_digest_pdf_url != "None":
                digest_pdf = fetch_pdf(bill_digest_pdf_url)
                if digest_pdf is None:
                    logger.warning("Failed to fetch bill digest for bill '%s'", bill_title)
                    continue
                pdfs.append(digest_pdf)

            completion = client.generate_content(
                prompt=bill_enrichment_prompt,
                pdfs=pdfs,
                response_schema=EnrichedBill.model_json_schema(),
                use_url_context=True,
            )
            output_dir = Path("completions") / "bill_enrichment" / MODEL_NAME
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{bill_title.replace(' ', '_')}.json"
            with output_path.open("w") as f:
                f.write(completion)
            logger.info("Wrote completion for bill '%s' to %s", bill_title, output_path)

            if idx < len(slice_rows) - 1:
                time.sleep(sleep_between_calls)  # Avoid rate limiting


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Run AI tasks for the project")
    parser.add_argument(
        "--task",
        choices=["bill_enrichment"],
        default="bill_enrichment",
        help="The AI task to run (only 'bill_enrichment' is supported currently)",
    )
    parser.add_argument(
        "--input_data_start_idx",
        type=int,
        default=0,
        help="Start index (inclusive) into the input data (default: 0)",
    )
    parser.add_argument(
        "--input_data_end_idx",
        type=int,
        default=None,
        help="End index (exclusive) into the input data. Omit for the end of the data.",
    )
    parser.add_argument(
        "--sleep_between_calls",
        type=int,
        default=20,
        help="Seconds to sleep between API calls (default: 30)",
    )

    args = parser.parse_args()

    if args.task == "bill_enrichment":
        run_bill_enrichment(
            input_data_start_idx=args.input_data_start_idx,
            input_data_end_idx=args.input_data_end_idx,
            sleep_between_calls=args.sleep_between_calls,
        )


if __name__ == "__main__":
    main()
