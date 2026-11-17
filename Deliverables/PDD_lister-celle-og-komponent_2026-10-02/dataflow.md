# Dataflyt — Mine lister: celle og listekomponent

Status: utkast ved G2 (2026-10-02). Hver kant skal finnes i `contract/lists_cell_contract_v0.json` (test.cells.dataflow-matches-contracts).

```
                           ┌──────────────────────────────┐
   «Mine lister»           │  Porthole (web eller app)     │
   CellConfiguration ─────►│  referanse my → cell:///Lists │
                           └──────┬───────────────▲───────┘
                     my.lists.* set│               │ my.lists.state get
                                  ▼               │
                           ┌──────────────────────┴───────┐      persistCellSnapshot
                           │  ListsCell  cell:///Lists     │─────────────────────────► resolverens persistens
                           │  (CellBase, eier = brukeren)  │◄──── encode/decode ─────  (eierens entitet)
                           └──────▲───────────────┬───────┘
         lists.* set + mount      │               │ lists.state.lists[n].mount
         {instanceID=listId}      │               ▼
                           ┌──────┴───────────────────────┐
   Vert med                │  ComponentSurface(sourceKeypath: mount, instanceIDKeypath: id)
   ComponentSurface ──────►│  rendereren monterer sjekklisten per liste
                           └──────────────────────────────┘
```

| # | Fra | Til | Kanal | Payload | Kontrakt |
|---|---|---|---|---|---|
| 1 | Porthole («Mine lister») | ListsCell | `get my.lists.state` → `lists.state` (+ nestet `…state.lists`, `…state.activeAsRows`, `…state.emptyHint`, `…state.notice`) | — | `get lists.state` |
| 2 | TextField «Ny liste …» | ListsCell | `set lists.list.create` | string | `ListCreateRequest` |
| 3 | List (liste av lister), radvalg | ListsCell | `set lists.list.select` | `{selected: id, trigger, selectedIndex, selectionMode}` | `ListSelectRequest` |
| 4 | TextField (listetittel) | ListsCell | `set lists.list.rename` | string → mål-liste | `ListRenameRequest` + targetListRule |
| 5 | Button (søppelkasse i tittelraden) | ListsCell | `set lists.list.remove` | `removeListPayload = {listId}` | `ListRef` |
| 6 | TextField «Legg til …» | ListsCell | `set lists.item.add` | string → mål-liste | `ItemAddRequest` + targetListRule |
| 7 | Button ○ / ✓ i punktrad | ListsCell | `set lists.item.toggle` | `togglePayload = {listId, itemId}` | `ItemRef` |
| 8 | Button ▲ / ▼ i punktrad | ListsCell | `set lists.item.move` | `moveUpPayload/moveDownPayload = {listId, itemId, direction}` | `ItemMoveRequest` (piler) |
| 9 | Dra rad → slipp på rad (web) | ListsCell | `set lists.item.move` | `{dragRole, dragPayload:{listId,itemId}, dropTargetRole, dropTargetPayload:{listId,itemId}, dropIntent, modifierActive}` | `ItemMoveRequest` (slipp) |
| 10 | Button 🗑 i punktrad | ListsCell | `set lists.item.remove` | `removePayload = {listId, itemId}` | `ItemRef` |
| 11 | Button «Fjern utførte» | ListsCell | `set lists.list.clearDone` | `clearDonePayload = {listId}` | `ListRefOrTrue` |
| 12 | ListsCell | resolver | `persistCellSnapshot(self)` etter hver ok-mutasjon; `lists_snapshot_unverified` i `notice` når gjenlesing feiler | Codable-tilstand | invariants |
| 13 | ListsCell | vert | `lists.state.lists[n].mount` / `lists.state.mountsById.<id>` = `SkeletonComponentMount{componentID: haven.lists.checklist, revision: 1, sourceCellEndpoint: cell:///Lists, skeleton: checklistSkeleton("lists."), item: ListView}` | — | `SkeletonComponentMount` |
| 14 | Montert sjekkliste (web) | ListsCell | samme som 4–11, men keypath uten `my.`-prefiks, sendt til `cell:///Lists` av Porthole-serveren med `mount` i `ComponentActionContext` (TaskLocal) | som over | targetListRule (valg A) |

Ikke med (egen pakke): Porthole-serverens pin av CellProtocol, menyoppføring, native vertsadapter for monterte handlinger, bro-transport av `mount`.
