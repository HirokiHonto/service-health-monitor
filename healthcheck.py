import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request,urlopen

def check_endpoint(url:str) -> dict:
    start = time.perf_counter()

    request = Request(
        url,
        headers={"User-Agent":"service-health-monitor/0.1"},
    )

    try:
        with urlopen(request,timeout=5) as response:
            status_code = response.status
            healthy = 200 <= status_code < 300
            error = None

    except HTTPError as exc:
        status_code = exc.code
        healthy = False
        error = str(exc)

    except (URLError, TimeoutError) as exc:
        status_code = None
        healthy = False
        error = str(exc)

    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "url":url,
        "healthy":healthy,
        "status_code": status_code,
        "response_time_ms": round(elapsed_ms,2),
        "error": error,
    }

if __name__ == "__main__":
    result = check_endpoint("https://example.com")
    print(json.dumps(result, indent=2))