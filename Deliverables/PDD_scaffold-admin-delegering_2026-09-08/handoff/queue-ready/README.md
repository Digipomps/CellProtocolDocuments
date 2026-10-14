# Jobber som er klare for køen, men bevisst ikke lagt inn

Legges i `_losen-queue/inbox/` når forutsetningen under er oppfylt. Kopier begge
filene med samme id.

## sad-wp1-registry-20260909

**Venter på:** et CellScaffold-arbeidstre som ikke er opptatt av en annen PDD.
Natt til 9. september sto treet på `pdd/tillitspakke-agentflaate` med 181 skitne
oppføringer. Å implementere WP1 der ville blandet to PDD-er i samme diff, og
Kjetil eier branch-hygienen — derfor ble jobben forberedt, ikke lagt inn.

Jobben har selv en forhåndssjekk som stopper på den branchen, så den er trygg å
legge inn: den vil avvise seg selv hvis forutsetningen fortsatt ikke holder.
