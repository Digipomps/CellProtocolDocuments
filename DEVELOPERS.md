# DEVELOPERS

Velkommen! Dette er inngangen for utviklere og assistenter (Codex/AI) til praktiske rutiner og lenker i prosjektet.

## SSH og Package Resolve (kritisk for Digipomps-repoer)
Se playbook:
- SSH_SETUP.md (i prosjektroten) — inneholder steg-for-steg for å fikse SSH/SwiftPM-problemer, inkludert known_hosts, ssh-agent/Keychain, Xcode/SwiftPM-cacher og diagnosekommandoer.

Direktelenker:
- [SSH_SETUP.md](SSH_SETUP.md)

## Onboarding og nyttige snarveier
- Åpne Xcode-prosjektet, og hvis pakker feiler/henger: følg SSH_SETUP.md først.
- Dersom du trenger mer kontekst i en Codex-tråd, referer til denne filen og SSH_SETUP.md.

## Retningslinjer for endringer
- Hold SSH_SETUP.md oppdatert når nøkkel-/repo-policy endres.
- Legg til flere seksjoner her (DEVELOPERS.md) for gjentatte oppgaver/rutiner som bør være synlige for både utviklere og assistenter.
## Docker: lokal bygging og remote deploy (dev.haven)

Denne seksjonen beskriver hvordan du bygger Docker lokalt og deretter deployer (bygger/kjører) på dev.haven.

### Forutsetninger
- Docker installert lokalt.
- Tilgang til dev.haven.digipomps.org (IP: 207.127.94.25) med privatnøkkel.
- Docker installert på serveren (kan aktiveres med systemctl, se under).

### SSH til dev.haven
Bruk denne kommandoen (som oppgitt):

```bash
ssh -i ~/.ssh/ssh-key-2025-03-20.key opc@207.127.94.25



