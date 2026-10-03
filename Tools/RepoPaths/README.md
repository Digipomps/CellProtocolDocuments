# haven_path — `Repo::sti` til presis full path

Formålet, og ingenting annet: **en referanse i et dokument skal gi entydig full
path uansett hvor repoene ligger på maskinen.** Strukturen i et repo er lik for
alle; hvor repoet ligger er en device-innstilling.

```
CellProtocolDocuments::Book/23_Purpose_Knowledge_Base.md
```

blir til den rette absolutte stien på hver maskin, uten at dokumentet endres.

## Oppsett, én gang per maskin

```bash
python3 Tools/RepoPaths/haven_path.py init ~/Build/Digipomps/HAVEN
python3 Tools/RepoPaths/haven_path.py check
```

`init` ser hva som faktisk finnes og skriver `~/.haven/repos.json`. Ingen
håndvedlikeholdt liste. Ligger et repo utenfor fellesmappen, settes en absolutt
`path` på den ene oppføringen — resten står.

## Bruk

```bash
haven_path.py path PalazzoScaffold::Tests/Roles/run_roles.py   # skriv full path
haven_path.py check                                            # alle repoer avledes
haven_path.py scan DOK.md …                                    # alle referanser i dokumentene
```

`$HAVEN_REPOS` eller `--config` velger en annen device-fil — for CI, for en VM,
eller for en kjøring låst til en worktree.

## Det den ikke gjør

Ingen leting, ingen fallback til søskenmappe, ingen gjetting fra `cwd`. En
referanse som ikke lar seg avlede navngir repoet og årsaken og gir exit ≠ 0:
`repo_not_declared`, `repo_missing`, `marker_missing`, `marker_mismatch`,
`escapes_repo`, `config_missing`, `config_invalid`.

Markøren er en identitetssjekk, ikke et bevis på riktig branch eller revisjon.

## At den kan bli rød

`check` mot en riktig maskin er ikke nok — en resolver som ignorerte konfigfila
og bare la sammen `commonRoot/<ID>` ville bestå på et konvensjonelt oppsett,
fordi det konvensjonelle oppsettet *er* `commonRoot/<ID>`. Derfor: pek `--config`
mot et lokke-tre der markørene er feil, og krev at hvert oppslag feiler.

```
$ haven_path.py --config /tmp/lokke/repos.json check
  FAIL CellProtocolDocuments::  marker_mismatch: … lacks '# CellProtocol Documentation Index'
  FAIL PalazzoScaffold::        repo_missing: … /tmp/lokke/finnes-ikke
0/2 repoer lot seg avlede
```

Målt 2026-09-09: samme referanse ga riktig full path både i Cowork-VM-en og på
et oppsett der repoene lå spredt under andre mappenavn, med bare device-fila
endret — og lokke-treet ga 0/2 med navngitte årsaker.

## Videre

Den fulle gjennomgangen av hvor konvensjonen brytes i dag, og en migreringsplan
i åtte steg, ligger i
`CellProtocolDocuments::Deliverables/Repo_Path_Konvensjon_2026-09-09.md`.
Dette verktøyet er det den planen kaller M1.
