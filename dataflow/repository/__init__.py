import logging
from typing import Optional

import apache_beam as beam
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_exponential


class GetCryptioApi(beam.DoFn):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def setup(self):
        self.http = httpx.Client(
            base_url="https://app-api.cryptio.co/api",
            headers={"accept": "application/json"},
            timeout=None,
        )

    def process(self, api_key: str):
        @retry(
            reraise=True,
            retry=retry_if_exception_type(httpx.HTTPStatusError),
            stop=stop_after_delay(60 * 5),
            wait=wait_exponential(multiplier=1, min=1, max=16),
        )
        def request(cursor: Optional[str]):
            r = self.http.get(
                self.endpoint,
                params={"cursor": cursor},
                headers={"cryptio-api-key": api_key},
            )
            r.raise_for_status()
            return r.json()

        cursor = None

        while True:
            logging.info(f"{self.endpoint}/{api_key}/{cursor}")

            response_data = request(cursor)

            _cursor = response_data["cursor"]

            yield {**response_data["data"], "api_key": api_key}

            if not _cursor:
                break
            else:
                cursor = _cursor
