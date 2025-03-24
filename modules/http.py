import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from modules.config import headers


class HttpClient(requests.Session):
    def __init__(self, base_url="", proxy=None):
        super().__init__()
        self.base_url = base_url
        self.headers.update(headers)

        if proxy:
            self.proxies.update({"http": proxy, "https": proxy})

        retry_strategy = Retry(
            total=5,
            status_forcelist=[502, 503, 504],
            backoff_factor=1,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    def _request(self, method, endpoint, *args, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return super().request(method, url, *args, **kwargs)

    def get(self, endpoint, *args, **kwargs):
        return self._request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self._request("POST", endpoint, *args, **kwargs)
