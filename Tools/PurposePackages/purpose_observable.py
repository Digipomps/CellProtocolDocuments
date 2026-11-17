"""Maskinlesbare mål på formål («observable», PDD formaal-som-gui-test, 2026-11-09).

Et formål som sitter på et GUI-element eller en cellehandling kan bære en liste
`observable`, hvert punkt et objekt med `kind` fra en lukket ordliste og de
argumentene ordet krever. En generisk kjører (Playwright for web, Swift for
celler) leser listen og utfører den; validatoren her avviser alt utenfor
ordlisten. Ordlisten utvides bare gjennom lærdomsregisteret, aldri ad hoc.
"""

# kind -> (påkrevde argumenter, valgfrie argumenter, hva kjøreren gjør)
VOCABULARY = {
    "opensTab": (("tab",), (), "Elementet aktiverer fanen `tab` (Tabs.activeTabStateKeypath blir lik tab)."),
    "dispatches": (("actionKeypath",), ("payloadShape",), "Elementet sender handlingen `actionKeypath`, eventuelt med nyttelast av formen `payloadShape` (objekt med nøkkel → type)."),
    "showsState": (("keypath",), ("equals",), "Verdien på `keypath` er synlig på flaten; med `equals` må den vise akkurat den verdien."),
    "insertsWidget": (("widgetKind",), (), "Elementet setter inn en komponent av typen `widgetKind` på flaten."),
    "navigatesTo": (("configuration",), (), "Elementet åpner konfigurasjonen `configuration` (navn eller UUID)."),
    "changesState": (("keypath",), ("equals",), "Handlingen endrer cellens tilstand på `keypath`; med `equals` til akkurat den verdien."),
}

ALLOWED_PAYLOAD_TYPES = {"string", "integer", "number", "bool", "object", "list", "null"}


def validate_observable(entry, where="observable"):
    """Returnerer en liste med feilmeldinger (tom = gyldig) for ett punkt."""
    errors = []
    if not isinstance(entry, dict):
        return [f"{where}: må være et objekt med 'kind', fikk {type(entry).__name__}"]
    kind = entry.get("kind")
    if kind not in VOCABULARY:
        return [f"{where}: ukjent kind '{kind}' — ordlisten er {', '.join(sorted(VOCABULARY))}"]
    required, optional, _ = VOCABULARY[kind]
    for arg in required:
        value = entry.get(arg)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{where}: {kind} krever '{arg}' som ikke-tom streng")
    for arg in entry:
        if arg != "kind" and arg not in required and arg not in optional:
            errors.append(f"{where}: {kind} kjenner ikke argumentet '{arg}'")
    shape = entry.get("payloadShape")
    if shape is not None:
        if not isinstance(shape, dict) or not shape:
            errors.append(f"{where}: payloadShape må være et ikke-tomt objekt nøkkel → type")
        else:
            for key, typ in shape.items():
                if typ not in ALLOWED_PAYLOAD_TYPES:
                    errors.append(f"{where}: payloadShape['{key}'] har ukjent type '{typ}' (tillatt: {', '.join(sorted(ALLOWED_PAYLOAD_TYPES))})")
    return errors


def validate_observables(container, where):
    """Validerer feltet `observable` på en node, en pakke-purpose eller en derivedTest."""
    if "observable" not in container:
        return []
    items = container["observable"]
    if not isinstance(items, list) or not items:
        return [f"{where}/observable: må være en ikke-tom liste"]
    errors = []
    for i, entry in enumerate(items):
        errors += validate_observable(entry, f"{where}/observable[{i}]")
    return errors


def describe(entry):
    """Én linje for mennesker, brukt i lookup og i TESTRESULT."""
    kind = entry.get("kind", "?")
    args = ", ".join(f"{k}={v!r}" for k, v in entry.items() if k != "kind")
    return f"{kind}({args})"
