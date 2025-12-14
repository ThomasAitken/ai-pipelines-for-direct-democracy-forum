import argparse
import csv
import logging
import time
from typing import Iterator

import requests
from requests.adapters import HTTPAdapter, Retry

from client import AIClient, MODEL_NAME
from prompts.bill_enrichment import EnrichedBill, prompt as bill_enrichment_prompt

logger = logging.getLogger(__name__)

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
            memo_resp = session.get(explanatory_memo_pdf_url)
            if memo_resp.status_code != 200:
                logger.error(f"Failed to fetch explanatory memo for bill '{bill_title}': HTTP {memo_resp.status_code}")
                continue
            pdfs = [memo_resp.content]
            if bill_digest_pdf_url != "None":
                digest_resp = session.get(bill_digest_pdf_url)
                if digest_resp.status_code != 200:
                    logger.warning(f"Failed to fetch bill digest for bill '{bill_title}': HTTP {digest_resp.status_code}")
                    continue
                pdfs.append(digest_resp.content)

            completion = client.generate_content(
                prompt=bill_enrichment_prompt,
                pdfs=pdfs,
                response_schema=EnrichedBill.model_json_schema(),
                use_url_context=True,
            )
            with open(f"completions/bill_enrichment/{MODEL_NAME}/{bill_title.replace(' ', '_')}.txt", "w") as f:
                f.write(completion)

            if idx < len(slice_rows) - 1:
                time.sleep(sleep_between_calls)  # Avoid rate limiting


def main():
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
