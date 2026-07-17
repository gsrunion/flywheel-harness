"""The mock endpoint is the harness's model-agnosticism proof: every harness
behavior must be testable against it with no model present. This suite pins the
mock's own /v1 contract so downstream integration tests can rely on it."""
import http.client
import json
import pathlib
import subprocess
import sys
import time

import pytest

MOCK = pathlib.Path(__file__).resolve().parents[1] / "mock" / "mock_llm.py"
PORT = 18089


@pytest.fixture(scope="module")
def mock_server():
    proc = subprocess.Popen([sys.executable, str(MOCK), str(PORT)])
    for _ in range(50):
        try:
            conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=1)
            conn.request("GET", "/health")
            conn.getresponse().read()
            break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("mock never came up")
    yield
    proc.kill()


def _post_chat(body):
    conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=5)
    conn.request("POST", "/v1/chat/completions", json.dumps(body),
                 {"Content-Type": "application/json"})
    return json.loads(conn.getresponse().read())


def test_models_listed(mock_server):
    conn = http.client.HTTPConnection("127.0.0.1", PORT, timeout=5)
    conn.request("GET", "/v1/models")
    data = json.loads(conn.getresponse().read())
    assert data["data"][0]["id"] == "mock-llm"


def test_completion_echoes_forwarded_request(mock_server):
    resp = _post_chat({"model": "any:role",
                       "messages": [{"role": "system", "content": "injected"},
                                    {"role": "user", "content": "ping"}]})
    echo = json.loads(resp["choices"][0]["message"]["content"])
    assert echo["received_model"] == "any:role"
    roles = [m["role"] for m in echo["received_messages"]]
    assert roles == ["system", "user"]


def test_usage_shape_present(mock_server):
    resp = _post_chat({"model": "m", "messages": []})
    assert set(resp["usage"]) >= {"prompt_tokens", "completion_tokens",
                                  "total_tokens"}
