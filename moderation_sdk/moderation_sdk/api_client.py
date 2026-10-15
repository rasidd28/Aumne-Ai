import json
import urllib.request
import urllib.error
from moderation_sdk.configuration import Configuration


class ApiClient:
    def __init__(self, configuration: Configuration = None):
        self.configuration = configuration or Configuration()

    def call_api(self, path: str, method: str = "GET", params: dict = None, body: dict = None):
        url = f"{self.configuration.host}{path}"
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
            if query:
                url = f"{url}?{query}"

        data = None
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if body is not None:
            data = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as err:
            err_body = err.read().decode("utf-8")
            try:
                detail = json.loads(err_body)
            except Exception:
                detail = err_body
            raise RuntimeError(f"HTTP {err.code}: {detail}") from err
