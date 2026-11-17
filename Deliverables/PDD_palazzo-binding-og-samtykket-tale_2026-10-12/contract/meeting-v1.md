# Foreslått møtekontrakt v1 — ikke implementert

purposeRef: purpose://candidate.palazzo-binding-og-samtykket-tale.consent

Planen binder sessionID, segmentID, monotont planRevision, planHash, formål, opptakeridentitet/enhet, eksakt deltaker- og mottakersett, operasjonene opptak/transkripsjon/midlertidig rålyd/levering, rute/språk, oppbevaringsfrister og tilbakekallingsvilkår. Godkjenning må være en autentisert, eksplisitt handling fra hver deltaker over samme hash/revisjon, med tidspunkt, utløp og unik operationID. Ingen tom deltakerliste, ukjent identitet, forhåndsavkryssing, taushet, transportaksept eller vertsoverstyring.

## Tilstandsmaskin

`draft → awaitingConsent → ready → recording → stopped → processing → delivering → complete | partial | expired | failed`

Avslag gir `declined`, uten opptak. Revokering eller roster-/planendring mens recording lukker opptaksgaten først. Deretter avsluttes segmentet og ny revisjon går til awaitingConsent med null ja. Tidligere segment behandles bare under sin opprinnelige plan. Nytt segment kan ikke starte automatisk. App-/celleomstart gjenoppretter aldri recording eller gamle leases.

`recording.start` validerer atomisk gjeldende revisjon, hash, hele deltakersettet, alle aktive grants og valgt opptaker; den gir tidsbegrenset tillatelse bundet til segment/epoch. Recorder revaliderer før første buffer, ved alle buffere og ved callbacks/finalisering. Gamle epoch-/revisjons-callbacks kan ikke legges i nytt segment. Stopp lukker innsamling før resten av UI/network-oppryddingen. ASR-finalisering av allerede godkjent lyd er en separat tillatt operasjon; ingen nye mikrofonbuffere etter stopp.

Alle kan stoppe. Lokal stopp/revokering virker på opptakeren straks den er mottatt. Fjernstopp og nettpartisjoner har eksplisitt bounded lease i PLAN; ingen påstand om null fjernforsinkelse. Ved ny deltaker skal møtet først få bekreftet stopp, så publisere nytt roster og be alle godkjenne. Ukjent fysisk person kan ikke oppdages sikkert automatisk.

## Explore/handlingsskisse

Get: `state`, `plan`, `participants`, `consents`, `recordingStatus`, `segments`, `deliveryStatus`, `transcript`, `trustPackage` — requester-avgrenset, ingen publisering i discovery.

Set: `plan.propose`, `roster.add`, `roster.change`, `invite`, `consent.approve`, `consent.decline`, `consent.revoke`, `recording.start`, `recording.stop`, `connection.retry`, `audio.retry`, `transcript.correction`. UI-navigasjon `view.*` og nearby refresh rutes av scaffold, ikke som ny opptaksmyndighet.

Payload fra de rendrerte knappene er en wire-skisse med sessionID, planRevision og fixture-operationID. Produksjonskontrakten legger til planHash/segmentID der handlingen trenger det og bruker autentisert requester. Feil: stalePlan, consentIncomplete, consentDeclined, unknownParticipant, expiredGrant, wrongRecorder, leaseExpired, unavailableAudio, forbiddenRecipient. Gjentatt identisk operationID gir samme resultat; ny bruk av samme ID med annet innhold avvises.

## Leveringskontrakt

Transkript-ID, versjon, hash, segmentID og felles trustPackage-hash bindes til eksplisitt godkjent mottakersett. Pakken inneholder minimerte identitetsreferanser, samtykkebevis, formål, rute, opptaksgrenser, usikkerhet, oppbevaring og slette-/leveringsstatus. Hemmelige nøkler, tokens, rålyd og andre deltakeres private personprofiler følger ikke med.

Transportattempt ≠ sent ≠ received ≠ persisted. Kvittering må komme fra riktig autentisert mottaker og binde innholdshash/versjon/segment. Duplikater dedupliseres på (segment, version, recipient), restart gir ikke ny autorisasjon. Alle inkludert opptakeren får sporbar privat mottakerkopi. Rettelse lager v2 med opprinnelse og ny levering under tillatt formål; ingen stille overskriving av felles v1.

Revokering stopper nye opptak og fremtidige ennå uutførte behandlinger/disclosures som den tilbakekalte tillatelsen dekker. En allerede mottatt kopi kan ikke påstås fjernslettet. Uavklart eller konfliktfylt distribusjonsmyndighet gir hold/avslag, ikke vertsoverstyring. UI skal forklare hvorfor «alle mottatt» da ikke kan oppfylles automatisk. Endring av mottakersett krever ny eksplisitt godkjenning fra berørte personer.

Oppbevaring/sletting må ha reell timer/sweep og kvittering per lagringssted. Lagring som ikke kan håndheve avtalt frist, er ikke støttet rute. Kildeinnhold slettes ikke bare fordi en release-metode returnerte det; outbox beholder autorisert kopi til receipt eller avtalt utløp. Rålydens selvstendige maksimumsfrist gjelder uansett leveringsstatus.

## Uforanderlig pakke og nye statushendelser

Basis-tillitspakken er uforanderlig og hashes sammen med transkriptversjonen. Senere leverings- og slettekvitteringer lagres i en separat signert, append-only statuslogg som refererer til basispakkens hash. UI merker tidspunkt/kilde for status. Endres basisinnhold eller transkript, opprettes ny eksplisitt versjon med ny hash; ikke en stille oppdatering under gammel hash. Lengre mottakeroppbevaring krever separat aktiv godkjenning fra alle i segmentets opprinnelige deltakersett.
