# Handoff — felles regler for utførere i denne oppgaven

Gjelder Codex-jobber i `_losen-queue` og alt arbeid på Mac-en. Stier relative til `HAVEN/`.

1. **Bygg i Codex-sandkassen:** `swift build --disable-sandbox --build-tests`, **uten**
   `arch`-prefiks. Kjør tester med
   `xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/<Pkg>PackageTests.xctest` —
   `swift test` velger x86_64-lasteren og feiler.
2. **Ingen git-mutasjon fra Cowork-VM-mounten.** Mounten nekter `rmdir`/`unlink`, så git
   kan ikke fjerne `.git/index.lock`. Commits gjøres av Codex eller Kjetil på Mac.
3. **Jobbfiler:** skriv `.prompt.md` først, `.job` sist, og `.job` som `mv` fra en tmp-fil i
   samme mappe. `.job` er signalet om at jobben er klar.
4. **`workspace-write` hvis jobben skal skrive noe**, og leveransestien på linje 3. Sett
   `cwd` til HAVEN-rot med mindre du har en grunn til å snevre inn.
5. **Én jobb, ett formål.** Blandede jobber gir svar der du ikke ser hvilken del som feilet.
6. **Bli på kandidatgrenen** til siste skive er ferdig. Verifiser at koden finnes før du
   bygger — «grønt bygg, 0 tester» betyr som regel at arbeidstreet er tomt.
7. **Forhåndssjekker navngir filer, teller dem aldri.** En sjekk som krever «6 filer»
   blokkerer falskt så snart en syvende legges til.
8. **Baseline måles på rent utsjekk fra `origin/main`**, aldri på en annen PDDs gren.
9. **Ingen hemmeligheter** i kode, fixtures, logger eller `TESTRESULT.md`.
10. **Skriv `ukjent` framfor å gjette.** En auditrad som sier `unavailable` skal oppgi
    hvilke stier som faktisk ble gjennomsøkt — hele HAVEN-treet, ikke bare de berørte
    repoene (lesson 2026-09-11).
11. **En konformansprøve beviser bare noe innenfor fordelingen den trekker fra.** Skriv ned
    trekkfordelingen, ikke bare resultatet.
12. **Push, `gh workflow run` og `sudo` på vert er Kjetils alene.** Ingenting meldes
    «deployet» eller «fikset» før det er verifisert med bevis.
