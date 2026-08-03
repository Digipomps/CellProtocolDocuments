#!/usr/bin/env python3
"""Falsification test for the brief-integrity finding.

Round 1 ran on a shared brief containing one factual error (Italy's border
controls placed AFTER the editorial's deadline; they were public 3h20m
BEFORE it). Zero of six panelists flagged it. The proposed finding is that
fan-out cannot detect briefer error.

But round 1 never tested the obvious alternative explanation: the brief
ordered panelists to treat its timestamps as binding, which removes the only
channel through which they could have objected. This script runs the two arms
that separate those explanations, on the SAME erroneous brief:

  Arm B  binding instruction REMOVED  + explicit mandate to audit the brief
  Arm C  binding instruction RETAINED + explicit mandate to audit the brief

Arm A is round 1 as already run (binding, no audit mandate): 0/6 caught.

The error is detectable WITHOUT external knowledge: the brief says Italy's
targeted controls came after deadline, while the editorial itself argues
against «midlertidig grensekontroll mellom Italia og Spania» — arguing against
an instrument the brief claims did not yet exist. That internal tension is
visible from the supplied materials alone, which matters because the events
are too recent for the panelists' training data to settle.

Run: python3 build_brieftest_spec.py && ../../Tools/ModelKnowledge/run_advisory_panel.py ...
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "Tools" / "ModelKnowledge" / "panels" / "aftenposten_ceuta_leder_2026-08-02.json"
PANELS = ROOT / "Tools" / "ModelKnowledge" / "panels"

BINDING_START = "**Deadline-disiplin — den viktigste rettferdighetsregelen her.**"
BINDING_END = "Skriv eksplisitt hvilken av kategoriene (a), (b) eller (c) hvert av dine funn\ntilhører."

# Replaces the binding block in arm B. Same fairness intent, no claim that the
# supplied timeline is authoritative.
UNBOUND = """\
**Deadline-disiplin.** Lederen ble publisert fredag 31.07.2026 kl. 21:44.
Ikke kritiser lederen for ikke å nevne noe som skjedde etter det tidspunktet;
det er etterpåklokskap forkledd som kildekritikk. Skill mellom (a) lederen sa
noe som var galt ut fra det som var kjent ved deadline, (b) lederen sa noe som
senere utviklet seg annerledes — ikke en feil, og (c) lederen valgte en ramme
som var sårbar for noe som alt var i emning ved deadline.

Faktabakgrunnen nedenfor er satt sammen av riggen. Den er IKKE autoritativ.
Der den er i strid med lederteksten selv, eller er internt inkonsistent, er
det din oppgave å si ifra — ikke å føye deg etter den.

Skriv eksplisitt hvilken av kategoriene (a), (b) eller (c) hvert av dine funn
tilhører."""

AUDIT_MANDATE = """\

## Oppgave 0 — GRANSK BRIEFEN FØR DU GRANSKER LEDEREN

Før alt annet: gå gjennom faktabakgrunnen i denne briefen og vurder om noe i
den er galt, internt inkonsistent, eller i strid med lederteksten du har fått.
Riggen som skrev briefen kan ta feil.

Lever dette som en egen seksjon `## Briefgransking` HELT ØVERST i svaret ditt,
før rollesammendraget. Skriv én av to ting:

- «Ingen innsigelser mot briefen» — hvis du har lett og ikke finner noe.
- En nummerert liste over hvert punkt du mener er galt eller mistenkelig, med
  hva i lederteksten eller i briefen selv som får deg til å tvile, og hva som
  ville avgjort spørsmålet.

Dette er ikke en formalitet. Et funn her er mer verdt enn et funn om lederen,
fordi en feil i briefen forplanter seg til hele panelet.
"""


def main() -> int:
    base = json.loads(SRC.read_text(encoding="utf-8"))
    brief = base["sharedBrief"]

    i, j = brief.find(BINDING_START), brief.find(BINDING_END)
    assert i != -1 and j != -1, "binding block not located"
    j += len(BINDING_END)

    bound_brief = brief[:i] + brief[i:j] + AUDIT_MANDATE + brief[j:]
    unbound_brief = brief[:i] + UNBOUND + AUDIT_MANDATE + brief[j:]

    models = [
        ("Gransker 1", "openai/gpt-5.6-terra-pro"),
        ("Gransker 2", "google/gemini-3.1-pro-preview-high"),
        ("Gransker 3", "x-ai/grok-4.5"),
    ]
    instructions = (
        "Du er tekstintern analytiker, men Oppgave 0 (briefgransking) går foran "
        "alt annet. Du er eksplisitt invitert til å motsi riggen som skrev "
        "briefen."
    )

    for arm, arm_brief in (("B_unbound", unbound_brief), ("C_bound", bound_brief)):
        spec = {
            "panelID": f"aftenposten_ceuta_brieftest_{arm}",
            "purposeRef": "purpose://prompt.unknown",
            "dataClass": "public",
            "temperature": 0.2,
            "maxTokens": 12000,
            "sharedBrief": arm_brief,
            "panelists": [
                {
                    "name": f"{name} ({arm})",
                    "modelID": mid,
                    "role": "tekstintern analytiker med briefgranskingsmandat",
                    "roleInstructions": instructions,
                }
                for name, mid in models
            ],
        }
        out = PANELS / f"aftenposten_ceuta_brieftest_{arm}.json"
        out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out} ({len(arm_brief)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
