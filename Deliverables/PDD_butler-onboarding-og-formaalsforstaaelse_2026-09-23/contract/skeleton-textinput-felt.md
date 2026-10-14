# Kontrakt — to nye felt på `SkeletonTextArea` og `SkeletonTextField` (WP-S)

Status: foreslått 2026-09-23, godkjent retning av Kjetil (Q4 «Nye felt i CellProtocol»). Ikke implementert.

| Felt | Type | Betydning | Når feltet mangler |
|---|---|---|---|
| `placeholderKeypath` | `String?` | Keypath som gir plassholderteksten. Verdien leses som tekst; tom eller manglende verdi → `placeholder` brukes | `placeholder` brukes som i dag |
| `secure` | `Bool?` **eller** `secureKeypath: String?` | Skjuler inndata (web: `type=password` / `-webkit-text-security`; native: `SecureField`). Keypath-varianten gjør at samme felt kan bytte modus per steg | Vanlig inndata |

Regler (testes i paritetsmatrisen og i CellScaffold):

1. Dekoding er bakoverkompatibel: gamle konfigurasjoner uten feltene dekoder og rendres uendret.
2. Web og native gir samme plassholder for samme tilstand, og begge skjuler inndata når `secure` er sann.
3. Et felt med `secure` skal ikke vise verdien fra `sourceKeypath` i klartekst. Det viser tomt eller maskert, aldri teksten.
4. `secure` er en visningsegenskap og gir ingen lagringsgaranti. Hindringen mot at nøkkelen havner i transkript, `state` eller logg ligger i GuidedOnboarding og hub-veien, og testes der (test.onb.noekkel-aldri-i-logg).
5. En `TextArea` med `secure` rendres som ett linjefelt. Flerlinjet skjult inndata gir ikke mening.
