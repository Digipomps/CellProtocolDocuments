---
work_id: astra-benkstyrt-utvikling-deploy-ttl-20260917
status: READY
created_at: "2026-09-17T10:17:44Z"
updated_at: "2026-09-17T10:17:44Z"
from: codex
to: astra
repo: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments
base_ref: null
target_branch: null
owner: astra
integrator: astra
depends_on: []
pr: null
commit: null
---

# Vurder benkstyring fra utviklings-Mac til vert med begrenset, tidsavgrenset autoritet

Kjetils bestilling 17. september 2026:

> Be astra vurdere hva som skal til for å kontrollere hele utviklings og deployløpet fra benken - som strekker seg fra utviklings M5 macen min til verten. Hvor trenger vi å kjøre privilegerte prosesser og hvordan skal vi sørge for at disse bare gjør det de får lov til - og at tilganger ikke vokser ukontrollert - de må ha ttl. Jeg tenker at en blanding av formål og agreements vil hjelpe oss.

Dette bestiller en kildebasert arkitektur- og gjennomføringsvurdering. Det gir ikke autorisasjon til å installere hjelpere, endre policy/tilganger, utstede grants, kjøre deploy, rydde filer, endre git-refs eller implementere løsningen. Read-only undersøkelser og vurderingsdokumenter inngår. Bruk oppgavens eksisterende Astra-modell og kontekst.

## Formål og mål for vurderingen

1. Hele utviklings- og deployløpet skal kunne styres og etterprøves fra benken. Måles i denne vurderingen ved en komplett matrise over hvert trinn, utførelsessted, aktør, ressurs, nødvendig rettighet, håndhever, kvittering og benkfelt. Ukjente trinn skal være synlige med et konkret kildebehov.
2. Privilegier skal begrenses til det en konkret, autorisert handling trenger. Måles ved at hver foreslått privilegert operasjon har et avgrenset grensesnitt, en navngitt autoritetskilde og en kontroll på utførelsesstedet, samt minst ett positivt og ett negativt aksepttilfelle.
3. Autoritet skal ikke vokse gjennom tid, delegering, gjentatte jobber eller gjenbruk av godkjenninger. Måles ved eksplisitte regler for TTL, maksimal levetid, fornyelse, tilbakekalling, arvede begrensninger og opphør under kjøring. For hvert vern: oppgi hva som finnes i dag, hva som må bygges og hvordan virkningen kan kontrolleres fra benken.

Bruk eksisterende purpose-identifikatorer dersom de passer og er kontrollert mot kildene. Ikke finn på kanoniske identifikatorer, schemaer eller støttede API-er. Skill brukerens formål fra påstander om hvilke mekanismer som virker.

## Startgrunnlag og premisskontroll

Du er den eksisterende Astra-oppgaven «Kartlegg feil i deploykjeden». Ditt tidligere svar ligger i:

- `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ASTRA-prosessgjennomgang-2026-09-17-SVAR.md`
- Etterkontroll: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ASTRA-prosessgjennomgang-2026-09-17-ETTERKONTROLL.md`
- Auditpost: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/queue/tasks/HD-0095.json`

Ved avsenderens kontroll i denne økten finnes 17 avventende poster under HD-0095. Etterkontrollens SHA-256 er `c5ca50fc99cb870992973bd904c619cc4b5e35db6a2c913012e242e858cd7ec5`. De nye F16/F17 gjelder henholdsvis staging-bevis ved produksjonsinngangen og kanonisk avgrensning av ryddeoperasjoner. Kilderevisjoner og tidligere registertall står i rapporten; de skal ferskhetskontrolleres før gjenbruk. M5 er brukeroppgitt, ikke maskinmålt av avsender.

Begynn med «Brief audit»: identifiser feil, ubegrunnede premisser og motstridende kilder i denne bestillingen og i auditene. Faktapåstandene er ikke bindende. Særlig er faktisk visning i begge benker fortsatt uverifisert (F13); ikke anta at statusprodusent innebærer fungerende konsument. HAVEN-Deploy manglet remote/origin/main ved forrige kontroll; dokumenter hvilket lokalt eller versjonert datagrunnlag du faktisk bruker.

Kjetils hypotese om **formål + agreements** skal prøves, ikke vedtas på forhånd. Undersøk hva kombinasjonen kan binde og bevise, hvor den bare beskriver hensikt, og hvilken konkret kapabilitet og OS-/runtime-kontroll som fortsatt trengs. Søk også motbevis: en korrekt beskrevet og gyldig avtale kan være for vid, feil oversatt til en privilegert operasjon eller ikke tilbakekalt på utførelsesstedet.

## Hva vurderingen skal dekke

### Hele løpets utførelsessteder

Kartlegg benk/UI, planlegging/HD-kø, Claude/Codex-utførere, lokal checkout og isolerte arbeidsrepoer, avhengighetshenting, bygg/test, eventuell signering/installasjon, git/PR/CI, artefaktpublisering, registry, transport til vert, prefetch, staging, produksjonspromotering, secret/config-håndtering, restart, rollback, kvitteringer og eventuell retensjon/rydding. Avgrens hva som er nødvendig for denne leveransen og hva som er eget framtidig arbeid.

For hvert trinn: trenger det vanlige brukerrettigheter, særskilt fil-/nettverkstilgang, en tjenesteidentitet, CI-/registry-capability, OS-admin/root eller ingen ny tilgang? Skill Codex-sandkasse, macOS-personvern-/autorisasjonsgrenser, Unix-rettigheter, Docker-kontroll og CellProtocol-policy. Tilgang utenfor en agents sandkasse er ikke automatisk behov for root. Skill langlivet tjenesteprosess fra kortlivet rett til en bestemt operasjon.

### Privilegerte grensesnitt og håndheving

Vurder en minimal lokal/vertsbasert privilegert hjelper med typede, avgrensede handlinger mot alternativer. Forklar hvor autoritet utstedes, hvem som kan utstede den, og hvor den sjekkes rett før effekten. Vis koblingen mellom domeneidentitet, formål, agreement, vilkår, konkret capability/grant, ressurs og utfører. Benk, prompt, QR/lenke eller transportkvittering skal ikke alene regnes som autoritet.

Behandle kanoniske filstier, symlinker, TOCTOU, endrede skript etter godkjenning, eksakt commit/image-identitet, replay/idempotens, feil vert/miljø og confused-deputy-problemer. En tillatt skriptsti gir ikke nødvendigvis kontroll over hva et senere endret skript gjør. Undersøk hvem som får installere/oppdatere hjelperen og endre policy; utføreren skal ikke kunne utvide egne tillatelser gjennom disse veiene.

### TTL og vern mot voksende tilgang

Foreslå en eksplisitt livssyklus for tildeling, aktivering, bruk, utløp, tilbakekalling og eventuell fornyelse. Begrunn anbefalte TTL-klasser og maksimumsverdier; ikke presenter dem som allerede besluttet av Kjetil.

Undersøk minst:

- Identitets-/domene-/ressurs-/handlings-/artefaktbinding, `notBefore`/`expiresAt`, eventuell lease og engangsbruk.
- Delegering som bare kan snevre inn scope og aldri overleve eller utvide foreldreautoriteten; begrens delegeringsdybde og eventuell videreutstedelse.
- Fornyelse uten stille forlengelse til permanent tilgang: hvem kan fornye, på hvilket ferskt grunnlag, med hvilken samlet maksimal varighet og hvilke kvoter?
- Tilbakekalling gjennom hele grant-kjeden, også på andre maskiner; offline eller utilgjengelig autorisasjonskilde, klokkeavvik, omstart og gamle cacher.
- Skillet mellom token-utløp og rettigheter som allerede er materialisert som åpen fil, prosess, socket, SSH-sesjon, Docker-jobb, midlertidig fil eller kopiert credential. TTL på et token alene er ikke et bevis på at slik autoritet opphører.
- Utløp eller tilbakekalling mens et langt bygg, en deploy eller en rollback pågår: konkrete sikre stoppunkter, fornyelsesregel og eventuell på forhånd avgrenset kompensasjonsrett. Ingen ubetinget «rollback får alltid lov» og ingen ukritisk prosessdreping midt i en transaksjon.
- Automatisk inventar over aktive/foreldede tillatelser, opprydding av midlertidig autoritet og deteksjon av varige ACL-/sudoers-/nøkkelendringer som omgår TTL-modellen.

### Benken og bevisene

Beskriv hva Kjetil og agentene faktisk skal kunne gjøre/se: be om en handling, forstå scope og konsekvens, se autoritetskilde og gjenstående TTL, se hvem som kan fornye/tilbakekalle, avbryte, følge delegert arbeid og kontrollere faktisk effekt. Bruk eksisterende tre baner i `haven.deploy.status.v1`; skill livssyklus, kontrollutfall og autoritet. Navngi additive felt som forslag dersom de mangler.

Hvert nødvendig tiltak skal ende i benken med maskinlesbar kontroll og kildebundet kvittering. Oppgi utfører (`codex`, `claude-local`, `claude-cloud`, `cell`) og hvor den må kjøre. Unngå «Kjetil limer inn et skript» som permanent driftsløsning. Reelle menneskelige beslutninger eller plattformkrav skal identifiseres konkret, ikke skjules.

## Kildekrav og forventet leveranse

Bruk relevante sikkerhets-, integrasjons-, transport- og formålsferdigheter. Les faktiske implementasjoner av Agreement/Condition/capability og resolver, HavenAgentD/agent-jobber, HAVEN-bro/tilgangsport, HD-dispatch/status og vertens deploy-/sudo-grensesnitt. Lokale kilder skal ha fil:linje og revisjon/hash. Verifiser aktuelle OS-/produktmekanismer i offisiell Apple-, systemd-, OpenSSH-, Docker-, GitHub- eller OpenAI-dokumentasjon der slike fakta er bærende. Ikke bruk en repoanalyse-mal som forbyr nødvendige kilder eller avgrenser bort Mac/vert-sammenhengen brukeren ba om.

Lever i `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/ASTRA_benkstyrt_utvikling_deploy_TTL_2026-09-17/VURDERING.md`:

1. Konklusjon og Brief audit.
2. Diagram over benk, utførere, tillitsgrenser og kvitteringsvei.
3. Privilegiematrise for hele løpet med eksisterende/forslått/ukjent tydelig skilt.
4. Konkret, foreslått autoritetsmodell og TTL-livssyklus; vis eventuell kontrakt med et komplett eksempel på en tillatt og en nektet operasjon.
5. Trussel-/akseptmatrise: positiv tilgang, feil domene/ressurs/artefakt, replay, utløp før/under kjøring, tilbakekalling, offline, restart, klokkeavvik, eskalerende delegasjon, selvfornyelse og scope-endring etter godkjenning.
6. Hva dagens formål/agreements/resolver faktisk kan håndheve, hvilke hull som krever ny implementasjon og hvor hypotesen ikke holder.
7. Minste sammenhengende implementeringsløp med avhengigheter, Benk-felt, utfører, akseptbevis og rollback per tiltak. Prioriter etter risiko og auditfunn; skill plattforminstallasjon fra normal drift.
8. Åpne spørsmål med navngitt eier/kildebehov og eksplisitt målstatus. Verifikasjon av designet er ikke sertifisering av en installert løsning.

Du eier VURDERING.md og nødvendige analysevedlegg i denne leveransemappen. BESTILLING.md er avsenderens bestilling; bevar den. Registrer vurderingsarbeidet og nødvendige oppfølgingsforslag i HAVEN-Deploy etter de lokale reglene, med kobling til HD-0095 og uten å overskrive de 17 auditpostene eller starte implementeringsjobber. Skriv kort kvittering i Losen-loggen. Ingen produktkode eller aktive privilegier skal endres.

Avsender gjør ikke parallell arkitektur- eller kodemutasjon mens du arbeider. Send til slutt en kort status med rapportsti, anbefalt autoritetsgrense, viktigste TTL-regler, eventuelle HD-ID-er og hva som fortsatt krever beslutning eller bevis.
