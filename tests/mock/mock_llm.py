#!/usr/bin/env python3
"""Mock OpenAI-compatible upstream for CI integration tests.

Echoes the received request (model + messages) back inside the completion
content, so tests can assert exactly what the proxy forwarded — e.g. that
context injection produced ONE merged system message, or that X-No-Context
suppressed it.
"""
import json
import http.server


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v1/models":
            self._send(200, {"object": "list",
                             "data": [{"id": "mock-llm", "object": "model"}]})
        elif self.path == "/health":
            self._send(200, {"status": "ok"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            self._send(400, {"error": "bad json"})
            return
        echo = json.dumps({
            "received_model": req.get("model"),
            "received_messages": req.get("messages", []),
        })
        self._send(200, {
            "id": "mock-1",
            "object": "chat.completion",
            "model": req.get("model", "mock"),
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": echo},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1,
                      "total_tokens": 2},
        })

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
