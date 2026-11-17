Kjoering `35704028290` — https://github.com/Digipomps/CellScaffold/actions/runs/35704028290

Logg: 4063 linjer.

## Linjer som ser ut som feil

```text
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:16.4359527Z   ✘   3 playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners (405ms)
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:39.5439130Z     Error: ^[[2mexpect(^[[22m^[[31mreceived^[[39m^[[2m).^[[22mtoEqual^[[2m(^[[22m^[[32mexpected^[[39m^[[2m) // deep equality^[[22m
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:39.5446558Z       245 |   await expect(page.locator("#porthole-skeleton-validation-error")).toContainText("forced candidate update failure");
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:39.5448657Z     > 247 |   expect(balance).toEqual({ added: 0, removed: 0 });
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:39.5454330Z     test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/test-failed-1.png
Focused control-plane gates	Run Admin web accessibility and responsive gates	2026-09-22T08:52:39.5471079Z   1 failed
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:54:53.1327226Z   ✘   2 playwright/butler-explicit-helper-placement.spec.js:16:5 › Butler explicit helper placement › desktop keeps the response in chat until the user opens one helper (24.4s)
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8801111Z     Error: ^[[2mexpect(^[[22m^[[31mreceived^[[39m^[[2m).^[[22mtoBe^[[2m(^[[22m^[[32mexpected^[[39m^[[2m) // Object.is equality^[[22m
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8806767Z     > 54 |       expect(beforeMetrics.composerInsideViewport).toBe(true);
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8809860Z       56 |       expect(sendBox.y + sendBox.height).toBeLessThanOrEqual(viewport.height + 1);
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8811120Z       57 |       expect(beforeMetrics.responseInsideDocument).toBe(true);
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8822850Z     test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/test-failed-1.png
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.8834505Z   1 failed
```

## Siste 60 linjer

```text
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9472746Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9474501Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9475579Z absorb feed. owner: D2654744-5933-4C0D-B978-C3F87732C46A
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9476091Z [ INFO ] POST /browserhead/porthole/action [request-id: 0F614170-A9AE-45D1-92B2-B3DF7BA49233]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9477246Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9478990Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9480270Z **** Creating BrowserClientIdentityVault for identitydDomain: 85B2E6E9-0905-4E41-969D-BD22454A8484
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9481127Z vaultURL: file:///tmp/tmp.MVUvqIMA2i/CellsContainer/PrivateVaults/85B2E6E9-0905-4E41-969D-BD22454A8484
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9481693Z Deiniting WebCellEmbeddings (81196740-B58B-4863-B069-F66C7BAE0CE3
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9482140Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9482547Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9482951Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9483365Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9483781Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9484213Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9484869Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9485299Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9485717Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9486131Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9486532Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9486934Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9487335Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9487733Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9488235Z [ INFO ] GET /browserhead/porthole/bootstrap [request-id: 3AF9949E-0596-47FE-955E-E86EACD5518E]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9489538Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9491471Z ********Reading sessionId: 81196740-B58B-4863-B069-F66C7BAE0CE3 sessions: ["73A079CF-2BA9-4377-A847-333EE8C26702": App.WebCellEmbeddings, "03A0EFF3-F290-4A9E-9887-D058F2E3907B": App.WebCellEmbeddings, "7EFC80AC-602F-4C8D-BBD8-57A08512D475": App.WebCellEmbeddings, "81196740-B58B-4863-B069-F66C7BAE0CE3": App.WebCellEmbeddings]
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9492669Z **** Creating BrowserClientIdentityVault for identitydDomain: 85B2E6E9-0905-4E41-969D-BD22454A8484
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9493339Z vaultURL: file:///tmp/tmp.MVUvqIMA2i/CellsContainer/PrivateVaults/85B2E6E9-0905-4E41-969D-BD22454A8484
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9493878Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9494274Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9494674Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9495079Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9495498Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9495925Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9496348Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9496763Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9497174Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9497583Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9497986Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9498390Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9498785Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9499199Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9499591Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9499984Z Did NOT find any EmitCell with name: TranscriptStore!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9500643Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9501067Z Did NOT find any EmitCell with name: PersonalIdentity!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9501474Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9501893Z Did NOT find any EmitCell with name: PersonalProfileDraft!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9502306Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9502718Z Did NOT find any EmitCell with name: PersonalPrivacyAudit!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9503128Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9503536Z Did NOT find any EmitCell with name: AppleIntelligence!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9503949Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9504335Z Did NOT find any EmitCell with name: EntityScanner!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9504721Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9505189Z Did NOT find any EmitCell with name: WorkflowStudio!!!
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9505563Z >> cancelled instantFeed publisher
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9505971Z Deiniting WebCellEmbeddings (81196740-B58B-4863-B069-F66C7BAE0CE3
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9506258Z 
Focused control-plane gates	Run Thursday demo P0 browser proof	2026-09-22T08:55:39.9507472Z ##[error]Process completed with exit code 1.
```
