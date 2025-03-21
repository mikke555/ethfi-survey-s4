import requests

from modules.config import headers


class HttpClient(requests.Session):
    def __init__(self, base_url="", proxy=None):
        super().__init__()
        self.proxy = proxy
        self.base_url = base_url
        self.headers.update(headers)

        if proxy:
            self.proxies.update({"http": proxy, "https": proxy})

    def _request(self, method, endpoint, *args, **kwargs):
        url = f"{self.base_url}{endpoint}"
        resp = super().request(method, url, *args, **kwargs)

        if resp.status_code not in [200, 201]:
            raise Exception(f"{resp.status_code} {resp.text}")

        return resp

    def get(self, endpoint, *args, **kwargs):
        return self._request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self._request("POST", endpoint, *args, **kwargs)
