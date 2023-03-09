import apache_beam as beam
import httpx


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
        cursor = None

        while True:
            r = self.http.get(
                self.endpoint,
                params={"cursor": cursor},
                headers={"cryptio-api-key": api_key},
            )
            r.raise_for_status()
            response_data = r.json()
            data = response_data["data"]

            if data:
                cursor = response_data["cursor"]
                yield data
            else:
                break
