# HAVEN — digital tools with people as the starting point

**What did you actually agree to?** Most of us don't know. We tap *accept* because we need to get on with things.

HAVEN is an open ecosystem under development, built on four rules for any service that wants to act for you:

1. **State the purpose** — explain the task before asking for anything.
2. **Ask for the least possible** — access should fit the task, not open everything.
3. **Give a receipt** — afterwards you can see what actually happened.
4. **Let yourself be stopped** — future use can be withdrawn.

This matters most when software acts on your behalf: booking, replying, agreeing, paying. Five questions should always be answerable — who asked for the action, what was the purpose, what was it allowed to do, how long did that last, and what actually happened?

## Maturity — read this before you read anything else

We date our claims and separate what is built from what is hoped for.

| | Status |
|---|---|
| Protocol building blocks (Cells, agreements, contracts, capability checks) | **Implemented, with targeted tests** |
| Connected user journeys (conference, profile, access surfaces) | **Prototype** — not ready for a public pilot |
| Democracy and value distribution | **Research direction** — no documented effect |

A good architecture does not guarantee good institutions, safe operations or fair outcomes. That has to be shown in each concrete use.

## Start here

- **[digipomps.org](https://digipomps.org)** — the project in plain Norwegian, with dated status labels, sources and a public corrections log
- **[Access-control proof](https://digipomps.org/bevis/tilgangskontroll/)** — one runnable test: a read is refused without a contract, allowed with a signed and limited one, and blocked when it tries to widen its own authority
- **[CellProtocol](https://github.com/Digipomps/CellProtocol)** — the Swift reference implementation the proof runs against

## Repositories

| Repository | What it is |
|---|---|
| [CellProtocol](https://github.com/Digipomps/CellProtocol) | Swift reference implementation: cells, agreements, contracts, capability checks, replay and audit |
| [PyCellProtocol](https://github.com/Digipomps/PyCellProtocol) | Python implementation and cross-runtime fixtures |
| [GoCellProtocol](https://github.com/Digipomps/GoCellProtocol) | Go implementation |
| [Binding](https://github.com/Digipomps/Binding) | SwiftUI/macOS shell that renders cell configurations natively |
| [CellProtocolDocuments](https://github.com/Digipomps/CellProtocolDocuments) | Specification chapters, the public website and claim documentation |
| [cellprotocol-admin-plane](https://github.com/Digipomps/cellprotocol-admin-plane) | Operator-facing administration surfaces |
| [CellUtility](https://github.com/Digipomps/CellUtility) | Shared utilities used across the Swift runtimes |
| [HAVEN_MVP](https://github.com/Digipomps/HAVEN_MVP) | Earlier end-to-end exploration, kept for reference |

Licensing differs across repositories, and some are public to read without a settled reuse licence. "Publicly readable" is not the same as "free to reuse" — see the open governance tasks on [digipomps.org/om](https://digipomps.org/om/).

## Who is behind this

HAVEN is managed by **Stiftelsen Digipomps**, an independent, politically unaffiliated Norwegian foundation established in 2019 (org. no. 922 135 134). Board: Kjetil Hustveit (chair and managing director), Petter Nielsen, Steinar Bjørlykke. The registration can be checked in [the Norwegian Register of Business Enterprises](https://virksomhet.brreg.no/nb/oppslag/enheter/922135134).

Being a foundation with open code does not make the work neutral. That is why we publish status, sources, limitations and corrections — and invite outside scrutiny.

The work has no external funding so far; it runs on the effort of the people doing it.

## Take part

Good objections are worth more than agreement. Open an issue, or write to **digipomp@digipomps.org** with the claim, the link and the best counter-evidence.

Other ways to contribute count too: taking part, practical help, sponsorship — or simply staying interested. We are at Arendalsuka, Norway's democracy festival, 10–14 August 2026.
