#!/usr/bin/env python3
"""
fixture_server.py -- a stand-in Palazzo, so the actor can be tested on itself.

This is not a mock of Palazzo's behaviour and must never be mistaken for one.
It is a stand for the ACTOR: five modes, each of which is a specific way a
harness can be wrong, so `selftest.py` can prove the actor notices. Pointing the
actor at the real server tells you about Palazzo; pointing it at this tells you
about the actor, and you need both before either answer means anything.

modes:
  normal            everything behaves; calibration passes
  broken-positive   the certain-to-be-reachable purpose is denied
  leaky-null        the certain-to-be-forbidden purpose is allowed
  ignores-principal every request succeeds whoever asks (the null run must catch it)
  unevaluable       a purpose answers 200 with a body the assertion cannot read
  null-leak         one non-calibration route answers anyone, so calibration
                    stays green and only the null-principal run can catch it
  unexpected-stop   a purpose the role file expects to reach is denied, with no
                    pre-declared meaning -- a human must judge it
  privacy-leak      a purpose declared forbidden is allowed
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

MODE = "normal"
CONSENTING = "consenting-guest-cell"


def route(principal: str, path: str, body: dict):
    """Return (status, payload). Deliberately small and explicit."""
    if MODE == "ignores-principal":
        return 200, {"value": {"items": [{}], "shared": [1, 2, 3, 4, 5]}}

    if path == "/api/scaffold/info":
        return 200, {"value": {"name": "fixture"}}

    if path == "/api/entity/state":
        if MODE == "broken-positive" and principal.startswith("guest:"):
            return 403, {"error": "denied"}
        return (200, {"value": {"id": principal}}) if principal.startswith("guest:") \
            else (403, {"error": "not a guest"})

    if path == "/api/house/staff":
        if MODE == "leaky-null" and principal.startswith("guest:"):
            return 200, {"value": {"staff": []}}
        return (200, {"value": {"staff": []}}) if principal == "house" \
            else (403, {"error": "denied"})

    if path == "/api/staff/brief":
        if not principal.startswith("staff:"):
            return 403, {"error": "denied"}
        cell = (body.get("value") or {}).get("guestCell")
        if MODE == "unevaluable":
            return 200, {}
        shared = [1, 2, 3, 4, 5] if cell == CONSENTING else []
        return 200, {"value": {"shared": shared, "notShared": 5 - len(shared)}}

    if path == "/api/staff/state":
        return (200, {"value": {}}) if principal.startswith("staff:") \
            else (403, {"error": "denied"})

    if path == "/api/cell/get" and MODE == "privacy-leak":
        # Leak exactly one keypath, and deliberately NOT the one the agent's
        # null calibration uses. Otherwise calibration catches it first and the
        # run never reaches its own judging -- which is what happened on the
        # first attempt at this fixture, and is itself worth knowing: the
        # calibration pair is the earlier and stronger check, and a leak it
        # does not happen to cover is the case exit code 5 exists for.
        if (body.get("value") or {}).get("keypath") == "entity.article.reactions":
            return 200, {"value": {"reactions": ["something private"]}}
        return 403, {"error": "denied"}

    if path in ("/api/insight/query", "/api/cell/get"):
        return 403, {"error": "denied"}

    if path == "/api/content":
        return 200, {"value": {"items": [{"id": "a1"}]}}

    if path == "/api/access/revoke":
        # Only the guest who owns the agreement may revoke it. A fresh principal
        # reaching this would be a real leak, and the null-principal run is the
        # only check that would notice -- so the stand-in must not be lax here.
        return (200, {"value": {}}) if principal == "guest:g1" \
            else (403, {"error": "denied"})

    if path == "/api/consent/state" and MODE == "unexpected-stop":
        # The role file expects to reach this and declares no meaning for a
        # stop, so the run must refuse to guess and hand it to a human.
        return 403, {"error": "denied"}

    if path in ("/api/entity/record", "/api/entity/article/react",
                "/api/guest/article/configuration", "/api/consent/state",
                "/api/access/state"):
        return (200, {"value": {}}) if principal.startswith("guest:") \
            else (403, {"error": "denied"})

    if path == "/api/house/remember/list" and MODE == "null-leak":
        # The failure the calibration pair cannot see: a route that answers
        # anyone, but is not one of the two purposes a role calibrates on.
        return 200, {"value": {}}

    if path in ("/api/house/remember/list", "/api/content/signals",
                "/api/content/publish"):
        return (200, {"value": {}}) if principal == "house" else (403, {"error": "denied"})

    return 404, {"error": "no such route"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _go(self, body: dict):
        principal = self.headers.get("X-Palazzo-Principal", "")
        status, payload = route(principal, self.path, body)
        raw = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self._go({})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            body = {}
        self._go(body)


def serve(port: int, mode: str):
    global MODE
    MODE = mode
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8099,
          sys.argv[2] if len(sys.argv) > 2 else "normal")
