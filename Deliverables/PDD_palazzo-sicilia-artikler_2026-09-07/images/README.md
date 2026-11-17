# images/ — G1-GUI for Sicilia-artiklene (mockups rendret fra skeleton/-JSON, 390×844, samme renderer og forbehold som PDD_palazzo-husk-det-jeg-sa/images/README.md)

| Bilde | Skeleton | Tilstand |
|---|---|---|
| gjest-sicilia-liste-v1.png | gjest-sicilia-liste.json | tre artikler publisert; trykk på kort åpner artikkelen (List single selection → guest.article.open) |
| gjest-sicilia-artikkel-v1.png | gjest-sicilia-artikkel.json | åpen artikkel: tekst, opphav, tre knapper, kommentarfelt, løftet «aldri at du leste» |
| gjest-sicilia-tom-v1.png | (seksjonen skjules) | ingen artikler publisert — flaten er som i dag |
| hus-artikkel-tagger-v1.png | hus-artikkel-tagger.json | husets utkast: én artikkel med foreslåtte tagger (samme flate som retter) |

Må verifiseres i Porthole: TextArea `submitActionKeypath` med fast payload (articleID, reaction: comment) — ellers egen keypath per artikkel.
