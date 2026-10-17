import time
from datetime import datetime, timezone

import requests


def check_website(url):
    start = time.perf_counter()

    result = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status_code": None,
        "latency_ms": None,
        "is_up": False,
        "error": None,
    }

    try:
        response = requests.get(url, timeout=10)

        result["status_code"] = response.status_code
        result["latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
        result["is_up"] = response.status_code < 500

    except requests.RequestException as exc:
        result["latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
        result["error"] = str(exc)

    return result
