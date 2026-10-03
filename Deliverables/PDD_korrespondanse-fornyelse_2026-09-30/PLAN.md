# PLAN: fornyelse av utløpt korrespondansetilgang

Planen følger formålene i FORMAALSSPEC §1. Hver arbeidspakke har en utfører og en test som skal bli grønn.

| AP | Formål | Hva som gjøres | Utfører | Test | Hva Kjetil gjør |
|---|---|---|---|---|---|
| AP1 | F1, F2, F3 | `enroll` lager en ny tilgangsforespørsel når tilgangen er utløpt og binder `renewsGrantID` | Losen | T1, T2, T3 | ingenting |
| AP2 | F4 | Korrespondansetestene og full testmengde kjøres mot baseline | Losen (via jobbløperen på Macen) | T4 | ingenting |
| AP3 | F5 | Grenen merges eller settes ut på staging. En ny invitasjon for `kjetil-vegar-codex-d` legges i miljøet. | Losen | T5 | sier ja til utsettingen |
| AP4 | F0, F5 | `setup` med den nye invitasjonen på Kjetils Mac. Godkjenning på adminsiden. `activate`. | Losen og Kjetil | T5 | godkjenner kortet på https://staging.haven.digipomps.org/admin/funding |
| AP5 | F0 | Vegar sender, og Kjetils innboks leses | Vegar og Losen | T5 | ber Vegar prøve igjen |
