from tester.client import http_get

BASE_URL = "https://api.agify.io"

def test_status_200():
    response, latency = http_get(f"{BASE_URL}?name=michael")
    ok = response is not None and response.status_code == 200
    return {"name": "GET /?name=michael - status 200",
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency,
            "details": f"status={response.status_code if response else 'timeout'}"}

def test_content_type_json():
    response, latency = http_get(f"{BASE_URL}?name=michael")
    ok = response is not None and "application/json" in response.headers.get("Content-Type", "")
    return {"name": "Content-Type JSON",
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency,
            "details": response.headers.get("Content-Type", "") if response else "no response"}

def test_champs_obligatoires():
    response, latency = http_get(f"{BASE_URL}?name=michael")
    if response is None:
        return {"name": "Champs obligatoires présents", "status": "FAIL", "latency_ms": None, "details": "no response"}
    data = response.json()
    missing = [f for f in ["name", "age", "count"] if f not in data]
    ok = len(missing) == 0
    return {"name": "Champs obligatoires présents",
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency,
            "details": f"missing: {missing}" if missing else "all fields present"}

def test_types_champs():
    response, latency = http_get(f"{BASE_URL}?name=michael")
    if response is None:
        return {"name": "Types des champs", "status": "FAIL", "latency_ms": None, "details": "no response"}
    data = response.json()
    errors = []
    if "name" in data and not isinstance(data["name"], str):
        errors.append("name should be string")
    if "age" in data and data["age"] is not None and not isinstance(data["age"], int):
        errors.append("age should be int or null")
    if "count" in data and not isinstance(data["count"], int):
        errors.append("count should be int")
    return {"name": "Types des champs",
            "status": "PASS" if not errors else "FAIL",
            "latency_ms": latency,
            "details": ", ".join(errors) if errors else "all types correct"}

def test_entree_invalide():
    response, latency = http_get(f"{BASE_URL}?name=")
    ok = response is not None and response.status_code in [400, 404, 422, 200]
    return {"name": "Entrée invalide (name vide)",
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency,
            "details": f"status={response.status_code if response else 'timeout'}"}

def test_nom_numerique():
    response, latency = http_get(f"{BASE_URL}?name=12345")
    ok = response is not None and response.status_code in [200, 400, 422]
    return {"name": "Nom numérique",
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency,
            "details": f"status={response.status_code if response else 'timeout'}"}

def test_latence():
    latencies = []
    for _ in range(5):
        response, latency = http_get(f"{BASE_URL}?name=anna")
        if latency is not None:
            latencies.append(latency)
    if not latencies:
        return {"name": "Latence (avg + p95)", "status": "FAIL", "latency_ms": None, "details": "no responses"}
    avg = round(sum(latencies) / len(latencies))
    p95 = sorted(latencies)[int(len(latencies) * 0.95) - 1] if len(latencies) > 1 else latencies[0]
    return {"name": "Latence (avg + p95)",
            "status": "PASS" if avg < 2000 else "FAIL",
            "latency_ms": avg,
            "details": f"avg={avg}ms, p95={p95}ms"}

def run_all():
    return [
        test_status_200(),
        test_content_type_json(),
        test_champs_obligatoires(),
        test_types_champs(),
        test_entree_invalide(),
        test_nom_numerique(),
        test_latence(),
    ]