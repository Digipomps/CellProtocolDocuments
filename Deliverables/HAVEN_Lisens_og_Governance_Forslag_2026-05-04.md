# HAVEN Lisens Og Governance - Forslag

Dato: 2026-05-04  
Status: Arbeidsforslag basert på Claude-svaret, justert for HAVEN/DiMy og senere juridisk gjennomgang.  
Viktig: Dette er ikke juridisk rådgivning. Bruk dette som grunnlag for advokat, styrevedtak og praktisk repo-oppsett.

## 1. Kort Anbefaling

HAVEN bør ikke ha en hjemmelaget "alt-i-ett"-lisens. Den ryddigste modellen er:

1. HAVEN-kode publiseres under Apache License 2.0.
2. Offisielle HAVEN-releaser styres separat av en HAVEN Ward.
3. HAVEN-navn, logo, "Official HAVEN", "HAVEN Certified" og tilsvarende kontrolleres separat gjennom varemerke-/brandpolicy.
4. Betaling for group identities, selskaper, organisasjoner, verifisering, drift eller hosted infrastruktur reguleres i egne servicevilkår, ikke i kodelisensen.
5. DiMy-kode holdes separat og får egen lisens.

Dette gir en praktisk balanse:

- Koden kan være reelt open source.
- Brukere kan bruke, lese, endre, forke og distribuere HAVEN.
- Stiftelsen Digipomps kan fortsatt kontrollere hva som er offisiell HAVEN.
- Stiftelsen Digipomps kan fortsatt kreve betaling for driftede tjenester, group identity-funksjonalitet, sertifisering eller infrastruktur.
- DiMy kan holdes utenfor Apache-2.0-grensen.

## 2. Presisering Av "Koden Eies Av Brukerne"

Det bør ikke stå juridisk at "koden eies av alle brukerne" med mindre dette faktisk er etablert gjennom opphavsrettsoverdragelser, stiftelsesvedtak eller annen juridisk struktur.

Anbefalt formulering:

> HAVEN is stewarded as a digital commons by Stiftelsen Digipomps and licensed so that everyone may use, study, modify, fork, and distribute the HAVEN code under the Apache License 2.0.

Norsk variant:

> HAVEN forvaltes som et digitalt allmenningprosjekt av Stiftelsen Digipomps og lisensieres slik at alle kan bruke, studere, endre, forke og distribuere HAVEN-koden under Apache License 2.0.

Dette er mer presist fordi opphavsretten fortsatt kan ligge hos Stiftelsen Digipomps, enkeltbidragsytere, tidligere rettighetshavere eller tredjepartsprosjekter, mens lisensen gir alle brede bruksrettigheter.

## 3. Juridisk Arkitektur

### Lag 1: Kodelisens

Anbefaling: Apache License 2.0, uendret tekst.

Kodelisensen skal gi rett til å bruke, kopiere, endre, kjøre, forke og distribuere HAVEN-kode. Den skal ikke skille mellom enkeltpersoner, selskaper, organisasjoner eller kommersiell/ikke-kommersiell bruk.

### Lag 2: Governance Og Ward

Governance beskriver bare hva som blir del av offisiell HAVEN. Den begrenser ikke forks.

Foreslått prinsipp:

> Anyone may fork HAVEN under the Apache License 2.0. Only changes reviewed and approved through the current HAVEN Ward become part of the official HAVEN distribution.

Nåværende Ward:

> The current approved HAVEN Ward is Stiftelsen Digipomps.

Ikke legg inn organisasjonsnummer eller detaljer om stiftelsens vedtekter før dette er verifisert.

### Lag 3: Varemerke, Navn Og Sertifisering

Apache-2.0 gir ikke varemerkerettigheter. Det bør utnyttes ryddig:

- Forks kan si "based on HAVEN" når det er sant.
- Forks kan si "implements the HAVEN protocol" eller "compatible with the HAVEN protocol" hvis det er sant og ikke villedende.
- Forks bør ikke kunne kalle seg "Official HAVEN", "HAVEN Certified", "HAVEN Ward Approved" eller bruke HAVEN-logo uten tillatelse.

Unngå å reservere generelle kompatibilitetsutsagn for bredt. Det er bedre å beskytte offisielle merker enn å hindre sannferdig teknisk omtale.

### Lag 4: Servicevilkår

Betaling for group identities hører hjemme i servicevilkår, ikke i kodelisensen.

Ryddig formulering:

> The HAVEN code license does not restrict use by organisations or group identities. However, access to official hosted HAVEN services, verified group identities, managed infrastructure, certification, support, quotas, or foundation-operated network services may be subject to separate service terms and fees.

Norsk:

> HAVEN-kodelisensen begrenser ikke bruk fra organisasjoner eller group identities. Tilgang til offisielle driftede HAVEN-tjenester, verifiserte group identities, forvaltet infrastruktur, sertifisering, support, kvoter eller stiftelsesdrevet nettverksinfrastruktur kan reguleres av egne servicevilkår og betaling.

### Lag 5: DiMy

DiMy må ha egen lisens og tydelig teknisk grense:

- Helst separat repo.
- Alternativt tydelig mappe, for eksempel `DiMy/` eller `Sources/DiMy/`, med egen `LICENSE`.
- Ingen DiMy-fil skal ha Apache-2.0 HAVEN-header hvis DiMy ikke skal være Apache-2.0.
- HAVEN `README`, `NOTICE` og rotlisens må si at DiMy er ekskludert.

## 4. Foreslåtte Repo-Filer

Minimum:

- `LICENSE`
- `NOTICE`
- `README.md`
- `GOVERNANCE.md`
- `CONTRIBUTING.md`
- `TRADEMARK.md`
- `THIRD-PARTY-NOTICES.md`
- `SECURITY.md`

Hvis REUSE/SPDX brukes strengt:

- `LICENSES/Apache-2.0.txt`
- eventuelle `LICENSES/MIT.txt`, `LICENSES/BSD-3-Clause.txt`, osv.
- `.reuse/dep5` eller `REUSE.toml` ved behov.

## 5. LICENSE

Anbefaling:

Bruk Apache License 2.0 uendret. Ikke rediger lisensen. Legg den i `LICENSE` i repo-roten.

Kilde:

- https://www.apache.org/licenses/LICENSE-2.0.txt
- SPDX-id: `Apache-2.0`

## 6. Foreslått Kildekode-Header

Kort standardheader for HAVEN-filer:

```text
// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors
```

For Swift-filer kan dette brukes direkte. For Markdown/JSON/YAML brukes passende kommentarformat eller REUSE companion files der filformatet ikke støtter kommentarer.

Lengre variant hvis ønskelig:

```text
/*
 * SPDX-License-Identifier: Apache-2.0
 * SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors
 *
 * This file is part of HAVEN.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

Anbefaling: Bruk kort SPDX-header pluss full `LICENSE` i repoet. Det gir mindre støy i filene og bedre maskinlesbarhet.

## 7. README-Lisensseksjon

Forslag til `README.md`:

```markdown
## License

HAVEN source code in this repository is licensed under the Apache License,
Version 2.0. See [LICENSE](./LICENSE).

HAVEN is stewarded as a digital commons by Stiftelsen Digipomps. The
Apache License 2.0 grants broad rights to use, study, modify, fork, and
distribute the code. It does not grant rights to the HAVEN name, logos,
certification marks, official release channels, hosted services, or
foundation-operated infrastructure.

The official HAVEN release process is described in [GOVERNANCE.md](./GOVERNANCE.md).
Use of HAVEN names, logos, and certification marks is governed by
[TRADEMARK.md](./TRADEMARK.md).

DiMy code, if present, is licensed separately and is not covered by the
HAVEN Apache-2.0 license unless explicitly stated in the relevant file
headers and DiMy license files.

Third-party notices are listed in [NOTICE](./NOTICE) and
[THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md).
```

## 8. NOTICE

Forslag:

```text
HAVEN
Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

HAVEN is stewarded as a digital commons by Stiftelsen Digipomps and
licensed under the Apache License, Version 2.0.

This product may include third-party software, documentation, or assets.
Required third-party attribution notices are listed in
THIRD-PARTY-NOTICES.md and/or THIRD_PARTY_LICENSES/.

DiMy components, where present, are licensed separately and are not
covered by the HAVEN Apache-2.0 license unless explicitly stated in the
relevant DiMy file headers and license files.

"HAVEN", "Official HAVEN", "HAVEN Certified", "HAVEN Ward Approved",
associated HAVEN logos, and related certification marks are governed by
TRADEMARK.md. The Apache License 2.0 does not grant trademark rights.
```

Merk:

Apache-prosjekter bruker `NOTICE` spesielt for required notices. Ikke fyll `NOTICE` med reklame eller generelle forklaringer hvis det skaper unødig compliance-støy. En kort `NOTICE` og en mer detaljert `THIRD-PARTY-NOTICES.md` er ofte ryddigst.

## 9. GOVERNANCE.md

Forslag:

```markdown
# HAVEN Governance

## Status

This document describes how the official HAVEN distribution is maintained.
It is not a software license. It does not restrict your rights under the
Apache License 2.0 to use, copy, modify, fork, run, study, or distribute
HAVEN code.

## Official HAVEN

"Official HAVEN" means software, releases, services, marks, or
certification states published or approved by the current HAVEN Ward.

Forks and independent distributions are welcome under the Apache License
2.0, but they are not official HAVEN unless approved by the HAVEN Ward.

## HAVEN Ward

HAVEN is stewarded as a digital commons. The HAVEN Ward is responsible for:

- reviewing and approving changes to the official HAVEN distribution;
- publishing official HAVEN releases;
- maintaining release integrity and security expectations;
- managing official HAVEN marks and certification claims;
- operating or appointing operators for official HAVEN services;
- updating governance documents through the process described here.

The current approved HAVEN Ward is Stiftelsen Digipomps.

## Changes To The Official Distribution

Anyone may fork HAVEN and make changes under the Apache License 2.0.
However, a change becomes part of the official HAVEN distribution only
when it is reviewed, approved, and published through the HAVEN Ward or
maintainers appointed by the HAVEN Ward.

## Major Governance Changes

Major changes should require a public proposal and explicit approval by
the HAVEN Ward. Major changes include:

- changing the HAVEN code license;
- changing the current HAVEN Ward;
- changing the official trademark/certification policy;
- changing the contribution model;
- moving canonical release channels.

Recommended policy: at least 30 days public notice for major governance
changes, unless a security emergency requires temporary action.

## Forks

The Apache License 2.0 permits forks. Forks must comply with the license
and may not misrepresent themselves as official HAVEN. See TRADEMARK.md.
```

## 10. CONTRIBUTING.md

Anbefaling nå: DCO som standard, med mulighet for CLA senere hvis Stiftelsen trenger relisensiering.

Forslag:

```markdown
# Contributing To HAVEN

Thank you for contributing to HAVEN.

## License Of Contributions

HAVEN uses inbound = outbound licensing. Contributions to HAVEN are
submitted under the same license as the project: Apache License 2.0,
unless a file explicitly states another license.

## Developer Certificate Of Origin

HAVEN uses the Developer Certificate of Origin (DCO) version 1.1.
By signing off your commits, you certify that you have the right to
submit the contribution under the project license.

Use:

    git commit --signoff

This adds:

    Signed-off-by: Your Name <your.email@example.org>

Pull requests without DCO sign-off may not be merged.

## Official Review

The HAVEN Ward, or maintainers appointed by the HAVEN Ward, decides what
is accepted into the official HAVEN distribution. Approval to merge is
not guaranteed.

This does not limit your right to maintain your own fork under the Apache
License 2.0.

## Third-Party Code

If your contribution includes code, text, data, media, or assets created
by others, disclose it in the pull request and preserve all required
copyright, license, and notice information.

Do not add code with unclear or missing license terms.

Generally acceptable licenses include MIT, BSD-2-Clause, BSD-3-Clause,
ISC, Apache-2.0, and MPL-2.0, subject to review.

GPL, LGPL, AGPL, proprietary, source-available, or custom-licensed code
requires explicit HAVEN Ward review before inclusion.

## DiMy Boundary

DiMy code is licensed separately. Do not add DiMy code to Apache-2.0
HAVEN source folders unless the HAVEN Ward has explicitly approved the
license boundary and file headers.
```

CLA-spørsmål for senere:

Hvis Stiftelsen Digipomps vil kunne relisensiere HAVEN senere, for eksempel fra Apache-2.0 til MPL-2.0 eller AGPL-3.0, er DCO alene sannsynligvis ikke nok. Da bør advokat vurdere en Contributor License Agreement.

## 11. TRADEMARK.md

Forslag:

```markdown
# HAVEN Trademark And Brand Policy

## Summary

HAVEN code is licensed under the Apache License 2.0. The HAVEN name,
logos, official release marks, and certification marks are not granted by
the code license.

This policy protects users from confusion and protects the integrity of
official HAVEN releases.

## Protected Marks

The following marks are reserved for use approved by the HAVEN Ward:

- HAVEN, when used as the name of the official project or official distribution;
- Official HAVEN;
- HAVEN Certified;
- HAVEN Ward Approved;
- HAVEN logos and visual marks;
- other marks later published by the HAVEN Ward as official HAVEN marks.

Trademark registration status must be verified separately. This policy
does not by itself guarantee registered trademark rights.

## Allowed Use Without Permission

You may:

- refer to HAVEN by name when discussing, teaching, reviewing, criticizing,
  comparing, or documenting the project;
- state that your software is based on HAVEN if that is true;
- state that your software implements or is compatible with the HAVEN
  protocol if that is true and not misleading;
- distribute unmodified official HAVEN releases with their original name,
  subject to the Apache License 2.0 and this policy.

## Modified Distributions

If you distribute a modified version of HAVEN, you must make clear that
it is not official HAVEN unless the HAVEN Ward has approved that status.

Modified distributions should use a different product name and should not
use HAVEN logos, "Official HAVEN", "HAVEN Certified", or "HAVEN Ward
Approved" without written permission.

You may truthfully state that your fork is "based on HAVEN" or "derived
from HAVEN".

## Uses Requiring Permission

Written permission is required to:

- call a modified distribution "HAVEN";
- use HAVEN logos in app icons, websites, packaging, marketing, or app stores;
- claim "Official HAVEN", "HAVEN Certified", or "HAVEN Ward Approved" status;
- imply endorsement by Stiftelsen Digipomps or the HAVEN Ward;
- register domains, companies, products, or marks that may confuse users
  about official HAVEN status.

## Certification

"HAVEN Certified" and "HAVEN Ward Approved" are granted only by the
HAVEN Ward through a published certification or approval process.

## Enforcement

The HAVEN Ward should focus enforcement on uses that confuse users,
misrepresent official status, misuse certification marks, or harm trust
in the official HAVEN ecosystem.
```

## 12. Servicevilkår-Prinsipper

Dette er ikke full Terms of Service, men prinsipper advokat kan bruke.

```markdown
# HAVEN Hosted Services - Licensing Separation

The HAVEN code license governs the code. It does not govern access to
foundation-operated hosted services.

Stiftelsen Digipomps may offer official HAVEN hosted services, including:

- managed identity infrastructure;
- verified individual identities;
- verified group identities;
- organisation/entity administration;
- hosted bridges, relays, registries, catalogs, or discovery services;
- certification and compatibility testing;
- support, uptime commitments, backups, monitoring, and operations.

Individual owner identities may receive some services free of charge.
Group identities, companies, organisations, institutions, or other
multi-entity identities may be subject to separate pricing, quotas, or
contract terms.

These service terms do not restrict anyone's rights under the Apache
License 2.0 to use, fork, modify, run, or distribute the HAVEN code
outside the official hosted service.
```

## 13. DiMy-Eksklusjon

Forslag til rottekst:

```markdown
# DiMy Exclusion

DiMy code is not licensed as part of HAVEN under Apache License 2.0
unless a DiMy file explicitly says so.

DiMy components, libraries, services, smart contracts, payment logic,
credit/entitlement logic, regulatory logic, or other DiMy-specific files
are licensed separately under DiMy's own license terms.

If DiMy code is present in this repository, it must be located in a
clearly marked directory and include its own LICENSE file and file-level
license headers.
```

Anbefaling: hold DiMy i separat repo hvis mulig. Det er tryggere enn "samme repo, annen mappe".

## 14. Tredjepartskode

Policy:

- Ikke importer kode uten lisens.
- Bevar eksisterende lisens- og copyright-notiser.
- Legg tredjepartslisenser i `THIRD_PARTY_LICENSES/`.
- Oppdater `THIRD-PARTY-NOTICES.md`.
- Bruk SPDX-identifikatorer der mulig.
- Kjør license scan før offentlig publisering.

Forslag til `THIRD-PARTY-NOTICES.md`:

```markdown
# Third-Party Notices

This file lists third-party code, documentation, assets, or data included
in this HAVEN distribution.

| Component | Source | License | Notes |
| --- | --- | --- | --- |
| ExampleComponent | https://example.com/project | MIT | Header preserved in source file |

Full third-party license texts are stored in `THIRD_PARTY_LICENSES/`.
```

## 15. Rent Offentlig Repo

Å lage et rent repo uten gammel historie er fornuftig for å fjerne støy, gamle branches, interne commits og sensitiv kontekst.

Men:

- rent repo fjerner ikke behovet for riktig rettighetsgrunnlag;
- rent repo fjerner ikke tredjepartsnotisplikter;
- rent repo bør ikke brukes til å skjule opprinnelse hvis det finnes reelle rettighetskrav;
- første commit bør inneholde lisens, notice, governance og tredjepartsnotiser samtidig som koden.

Forslag til første commit:

```text
Initial public release of HAVEN under Apache-2.0
```

## 16. Pre-Publication Checklist

- [ ] Styrevedtak i Stiftelsen Digipomps om Apache-2.0 for HAVEN-kode.
- [ ] Juridisk gjennomgang av Apache-oppsett, governance, trademark, servicevilkår og DiMy-grense.
- [ ] Avklar om DCO er nok eller om CLA trengs.
- [ ] Avklar om "HAVEN" kan varemerkeregistreres i relevante klasser og markeder.
- [ ] Lag komplett tredjepartsinventar.
- [ ] Fjern hemmeligheter, nøkler, tokens, private paths, persondata og interne systemnavn.
- [ ] Separer DiMy.
- [ ] Legg inn `LICENSE`, `NOTICE`, `README.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `TRADEMARK.md`, `THIRD-PARTY-NOTICES.md`, `SECURITY.md`.
- [ ] Legg inn SPDX-header i HAVEN-filer.
- [ ] Kjør `reuse lint` eller tilsvarende.
- [ ] Kjør license scan, for eksempel ScanCode/FOSSology-lignende verktøy.
- [ ] Sett branch protection, DCO-check og reviewkrav.
- [ ] Publiser offisiell canonical repo-url.
- [ ] Publiser servicevilkår separat fra kodelisens.

## 17. Spørsmål Til Advokat

1. Kan Stiftelsen Digipomps være juridisk Ward, rettighetshaver, trademark-holder og serviceoperatør innenfor vedtektene?
2. Bør HAVEN-varemerket registreres i Norge/EU, og i hvilke Nice-klasser?
3. Er Apache-2.0 ansvarsfraskrivelsen tilstrekkelig for norsk/EU-kontekst, særlig overfor forbrukere?
4. Er DCO nok under norsk opphavsrett og ideelle rettigheter, eller bør det brukes CLA?
5. Må CLA brukes hvis Stiftelsen senere ønsker relisensiering?
6. Hvordan bør servicevilkår skille juridisk mellom individuelle owner identities og group identities?
7. Hvordan skal GDPR-roller defineres for hosted HAVEN: behandlingsansvarlig, databehandler eller felles behandlingsansvar?
8. Hvordan bør DiMy-grensen formuleres for å unngå implisitt Apache-lisensiering?
9. Trengs egen forsikring eller ansvarsbegrensning for Stiftelsen som Ward?
10. Hvordan bør internasjonale forks og trademark-bruk håndteres?

## 18. Åpne HAVEN-Beslutninger

Disse bør avgjøres før offentlig publisering:

1. Skal HAVEN bruke Apache-2.0 eller MPL-2.0?
   - Anbefaling: Apache-2.0.
2. Skal bidrag kreve DCO eller CLA?
   - Anbefaling: DCO først, CLA bare hvis advokat/styre mener fremtidig relisensiering krever det.
3. Skal DiMy ligge i separat repo?
   - Anbefaling: ja, hvis praktisk mulig.
4. Hvilke ord skal reserveres som offisielle marks?
   - Anbefaling: "Official HAVEN", "HAVEN Certified", "HAVEN Ward Approved", logoer.
5. Skal "HAVEN-compatible" være reservert?
   - Anbefaling: ikke generelt. Tillat sannferdig teknisk kompatibilitetsomtale, men reserver sertifiserte/offisielle claims.
6. Hvilke hosted services skal være gratis for individuelle owner identities?
   - Må beskrives i servicevilkår, ikke lisens.

## 19. Kildegrunnlag

Relevante offentlige kilder som dette forslaget bygger på:

- Open Source Definition: https://opensource.org/osd
- OSI FAQ: https://opensource.org/faq/
- OSI common reasons for license rejection: https://opensource.org/licenses/common-reasons-for-rejection-of-licenses
- Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
- Apache guidance for applying Apache-2.0: https://www.apache.org/legal/apply-license
- Developer Certificate of Origin 1.1: https://developercertificate.org/
- SPDX License List: https://spdx.org/licenses
- REUSE Specification: https://reuse.software/spec-3.3/

