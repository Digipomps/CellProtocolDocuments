#!/usr/bin/env python3
"""Kjør hver fixture mot sitt skjema og si fra hvis noe ikke oppfører seg som navnet lover.

Navnekonvensjon: fixture_<kontrakt>_ok_*.json skal validere, fixture_<kontrakt>_nei_*.json
skal avvises. En negativ fixture som plutselig validerer er en ekte feil — da har skjemaet
sluttet å håndheve noe det var laget for å håndheve.

    python3 check_fixtures.py        # avslutter med 1 hvis noe avviker
"""
import glob
import json
import os
import sys

try:
    import jsonschema
except ImportError:
    sys.exit("jsonschema mangler: pip3 install jsonschema")

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMAS = {
    "trustedmodels": "trustedmodels_v1.json",
    "aigateway": "aigateway_contract_v1.json",
    "genesis": "entityanchor_genesis_v1.json",
}


def main():
    failures = 0
    checked = 0
    for key, filename in sorted(SCHEMAS.items()):
        schema = json.load(open(os.path.join(HERE, filename), encoding="utf-8"))
        jsonschema.Draft7Validator.check_schema(schema)
        validator = jsonschema.Draft7Validator(schema)
        for path in sorted(glob.glob(os.path.join(HERE, "fixture_%s_*.json" % key))):
            name = os.path.basename(path)
            expect_valid = "_ok_" in name
            doc = json.load(open(path, encoding="utf-8"))
            is_valid = validator.is_valid(doc)
            checked += 1
            if is_valid != expect_valid:
                failures += 1
                print("FEIL %-52s forventet %s, fikk %s" % (
                    name,
                    "gyldig" if expect_valid else "avvist",
                    "gyldig" if is_valid else "avvist"))
                if not is_valid:
                    for err in validator.iter_errors(doc):
                        print("     %s" % err.message)
            else:
                print("OK   %-52s %s" % (name, "gyldig" if is_valid else "avvist"))
    print("%d fixtures, %d avvik" % (checked, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
