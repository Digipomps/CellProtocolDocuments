# Plan

1. trust — Codex trust_root_renewal: begrenset operator-pinnet v2-migrering; syntetiske tester før reelle nøkler. Root verifiserer live eier, resolver/bro og publiserer separat staging med CAS/backup.
2. entity — Codex enrollment_gap_audit + root: les siste entitetsarbeid og bruk etablert signert opptak/varig bevis; kontroller manglende datakilde uten å gi tilgang.
3. terminal — root: bootstrap-standarder, konkret feilhåndtering og person-godkjenning integrert med CLI; test på Linux.
4. verifikasjon — root: ingen grønn påstand uten eksakt artefakt, reell respons og sluttstatus. Test full Sprout-regresjon, mål serveravhengigheter, behold åpent det som trenger passkey/kapasitet.

## dataflow

CLI → HTTPS descriptor → festet admin → signert bootstrap-intent → registrering → signert/autoriserende entitetsbevis → verifisert entitetsstatus. Presence/owner-attach inngår ikke som myndighet for en ny nøkkel.
