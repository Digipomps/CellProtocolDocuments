#!/usr/bin/env python3
"""Fail-closed release guard for the single HAVEN app entry in the hero."""

from __future__ import annotations

import argparse
import ipaddress
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ACTIVE_LABELS = {
    "public-app": "Installer HAVEN",
    "public-demo": "Åpne HAVEN-demoen",
    "homescreen-demo": "Legg HAVEN-demoen på hjemskjermen",
}


class AppEntryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.state: str | None = None
        self.actions: list[dict[str, object]] = []
        self._inside = False
        self._depth = 0
        self._root_tag: str | None = None
        self._current_action: dict[str, object] | None = None
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if "data-app-entry-state" in values:
            if self.state is not None:
                self.errors.append("Fant mer enn ett app-aktiveringspunkt i heroen.")
                return
            if tag != "section" or "hero" not in (values.get("class") or "").split():
                self.errors.append("data-app-entry-state skal stå på section.hero.")
            self.state = values.get("data-app-entry-state")
            self._inside = True
            self._depth = 1
            self._root_tag = tag
            return

        if not self._inside:
            return

        if tag == self._root_tag:
            self._depth += 1
        if tag == "a":
            action: dict[str, object] = {"attrs": values, "text": []}
            self.actions.append(action)
            self._current_action = action

    def handle_data(self, data: str) -> None:
        if self._inside and self._current_action is not None:
            text = self._current_action["text"]
            assert isinstance(text, list)
            text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self._inside:
            return
        if tag == "a":
            self._current_action = None
        if tag == self._root_tag:
            self._depth -= 1
            if self._depth == 0:
                self._inside = False


def normalized_text(action: dict[str, object]) -> str:
    text = action["text"]
    assert isinstance(text, list)
    return " ".join("".join(str(part) for part in text).split())


def action_attrs(action: dict[str, object]) -> dict[str, str | None]:
    attrs = action["attrs"]
    assert isinstance(attrs, dict)
    return attrs


def classes(action: dict[str, object]) -> set[str]:
    return set((action_attrs(action).get("class") or "").split())


def origin(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return None
    try:
        port = parsed.port
    except ValueError:
        return None
    if port is not None:
        return None
    return f"https://{parsed.hostname.lower()}"


def unsafe_hostname(hostname: str) -> bool:
    hostname = hostname.lower().rstrip(".")
    if (
        hostname == "localhost"
        or hostname.endswith(".localhost")
        or hostname.endswith(".local")
        or hostname.endswith(".test")
        or hostname.endswith(".invalid")
        or hostname.endswith(".example")
        or hostname == "new.haven.digipomps.org"
        or hostname.startswith("staging.")
        or ".staging." in hostname
        or hostname.startswith("preview.")
        or ".preview." in hostname
        or hostname.startswith("review.")
        or ".review." in hostname
    ):
        return True
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        return False
    return True


def validate_markup(html: str, allowed_origin: str | None = None) -> list[str]:
    parser = AppEntryParser()
    parser.feed(html)
    errors = list(parser.errors)

    if parser.state is None:
        return errors + ["Mangler data-app-entry-state på heroens aktiveringspunkt."]
    if parser.state not in {"blocked", *ACTIVE_LABELS}:
        errors.append(f"Ukjent app-entry-status: {parser.state!r}.")
    if len(parser.actions) != 2:
        errors.append(f"Heroen skal ha nøyaktig to handlinger; fant {len(parser.actions)}.")
        return errors

    first, second = parser.actions
    first_attrs = action_attrs(first)
    second_attrs = action_attrs(second)

    for number, attrs in enumerate((first_attrs, second_attrs), start=1):
        if "target" in attrs:
            errors.append(f"Hero-handling {number} må åpne i samme fane og kan ikke ha target.")
        if "button" not in (attrs.get("class") or "").split():
            errors.append(f"Hero-handling {number} mangler button-klassen.")

    if parser.state == "blocked":
        if allowed_origin:
            errors.append("Blocked-status skal ikke bruke --allow-origin.")
        expected = (
            ("Se et tidlig testbevis", "/bevis/tilgangskontroll/", "button-primary"),
            (
                "Mennesket først – ikke mennesket alene",
                "#mennesket-og-fellesskapet",
                "button-secondary",
            ),
        )
        for number, (action, (label, href, style)) in enumerate(zip(parser.actions, expected), start=1):
            attrs = action_attrs(action)
            if normalized_text(action) != label:
                errors.append(f"Blocked hero-handling {number} skal hete {label!r}.")
            if attrs.get("href") != href:
                errors.append(f"Blocked hero-handling {number} skal peke til {href!r}.")
            if style not in classes(action):
                errors.append(f"Blocked hero-handling {number} skal bruke {style}.")
        return errors

    if allowed_origin is None:
        errors.append("Aktiv app-CTA krever eksplisitt --allow-origin fra release-eier.")
        return errors

    normalized_allowed_origin = origin(allowed_origin)
    if normalized_allowed_origin is None or normalized_allowed_origin != allowed_origin.rstrip("/").lower():
        errors.append("--allow-origin må være en ren HTTPS-origin uten port eller sti.")

    label = ACTIVE_LABELS.get(parser.state)
    if label is not None and normalized_text(first) != label:
        errors.append(f"CTA-teksten for {parser.state} skal være {label!r}.")
    if "button-primary" not in classes(first):
        errors.append("App-CTA-en skal være heroens primærhandling.")

    href = first_attrs.get("href") or ""
    parsed_href = urlparse(href)
    href_origin = origin(href)
    if href_origin is None:
        errors.append("App-CTA-en må bruke en absolutt HTTPS-URL uten eksplisitt port.")
    elif unsafe_hostname(parsed_href.hostname or ""):
        errors.append("App-CTA-en peker til staging, review, lokal adresse eller IP.")
    elif href_origin != normalized_allowed_origin:
        errors.append("App-CTA-ens origin er ikke lik release-eierens eksplisitte allowlist-origin.")
    if parsed_href.username or parsed_href.password or parsed_href.fragment:
        errors.append("App-CTA-en kan ikke inneholde credentials eller fragment.")

    if normalized_text(second) != "Forstå HAVEN" or second_attrs.get("href") != "#velg-inngang":
        errors.append("Aktiv hero skal ha «Forstå HAVEN» som sekundærhandling.")
    if "button-secondary" not in classes(second):
        errors.append("«Forstå HAVEN» skal være sekundær når app-CTA-en er aktiv.")
    return errors


def check_live_target(url: str, allowed_origin: str) -> list[str]:
    request = urllib.request.Request(url, headers={"User-Agent": "HAVEN-app-entry-release-guard/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            final_url = response.geturl()
            status = response.status
    except Exception as error:  # pragma: no cover - depends on live network
        return [f"Live-kontroll feilet: {error}"]
    errors: list[str] = []
    if status != 200:
        errors.append(f"Installasjonssiden svarte HTTP {status}, ikke 200.")
    if origin(final_url) != origin(allowed_origin):
        errors.append(f"Redirect endte på ikke-tillatt origin: {final_url}")
    return errors


def main() -> int:
    default_index = Path(__file__).resolve().parents[1] / "index.html"
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--html", type=Path, default=default_index)
    argument_parser.add_argument("--allow-origin")
    argument_parser.add_argument("--check-live", action="store_true")
    args = argument_parser.parse_args()

    html = args.html.read_text(encoding="utf-8")
    errors = validate_markup(html, args.allow_origin)
    parser = AppEntryParser()
    parser.feed(html)

    if args.check_live:
        if parser.state == "blocked":
            errors.append("Live app-kontroll kan ikke kjøres mens CTA-status er blocked.")
        elif not args.allow_origin or not parser.actions:
            errors.append("Live app-kontroll krever aktiv CTA og --allow-origin.")
        else:
            href = action_attrs(parser.actions[0]).get("href") or ""
            errors.extend(check_live_target(href, args.allow_origin))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: HAVEN app-entry er {parser.state}; heroen har to handlinger.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
