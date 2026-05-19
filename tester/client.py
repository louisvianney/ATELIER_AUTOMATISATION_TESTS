import time
import requests

def http_get(url, timeout=3, retries=1):
    for attempt in range(retries + 1):
        try:
            start = time.time()
            response = requests.get(url, timeout=timeout)
            latency_ms = round((time.time() - start) * 1000)
            if response.status_code == 429 and attempt < retries:
                time.sleep(2)
                continue
            return response, latency_ms
        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(1)
                continue
            return None, None
        except requests.exceptions.RequestException:
            return None, None
    return None, None