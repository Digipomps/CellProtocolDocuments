# test.lagring.rundtur og test.lagring.les-bytene mot S3-kompatibel testtjeneste

2026-10-08 · Losen (tråden «Fillagring for mediafiler») · Kode: PR #290 (`claude/lagringscelle-s3-20261008`, `cadf056`). Filen er egen for ikke å skrive i TESTRESULT.md som PR-tråden eier.

## Oppsett
- Kode: `ObjectStorageS3.swift` fram til `// MARK: - Nøkkeloppslag`, uten `import CellBase`, i en egen Swift-pakke med swift-crypto. Cellen selv (`ObjectStorageAdapterCell`) er ikke kjørt her.
- Kompilator: `swift:6.1-noble`, samme image som CI (`.github/workflows/admin-scaffold-image.yml:38`).
- Tjeneste: SeaweedFS (`chrislusf/seaweedfs:latest`) med S3-gateway og nøkkelkontroll. Anonym tilgang gir 403. Region `hel1`, path-style. Kjørt i Losens sky-container, ikke på Mac-en eller verten. MinIO-imaget kunne ikke hentes (`minio/minio` finnes ikke lenger på Docker Hub, og quay.io er sperret).
- Uavhengig leser: boto3.

## Funn før testen
`canonicalQuery` kompilerer ikke på Linux: «the compiler is unable to type-check this expression in reasonable time» (S3.swift:164, både debug og release). Rettelse og funn står i kommentaren på PR #290: https://github.com/Digipomps/CellScaffold/pull/290#issuecomment-6056000182. Testene under er kjørt med den rettelsen.

## Utdata (ordrett)
```
PASS headBucket
PASS feil nøkkel avvises http_403
PASS put/get/head rundtur/1kb.bin sha=true len=1024
PASS put/get/head rundtur/mappe med mellomrom/fil+pluss.bin sha=true len=4096
PASS put/get/head rundtur/æøå/ÆØÅ-lyd (1).mp3 sha=true len=4096
PASS put/get/head rundtur/tilde~og=lik&og.bin sha=true len=4096
PASS put/get 8 MB 39319caeb84c2563bf9c164041f0073f6134a2ab13a3da3c8b035cce41e1403f
PASS delete, deretter head = nil
PASS get ukjent = notFound not_found
FAILURES 0
uavhengig lesing 8 MB (boto3): 39319caeb84c2563bf9c164041f0073f6134a2ab13a3da3c8b035cce41e1403f
50 MB: PUT=200 (0.9 s) head=52428800 forventet=52428800 sha-lokal=6389ba69…c552 sha-via-signert-GET=6389ba69…c552 sha-boto3=6389ba69…c552 PASS
500 MB: PUT=200 (5.1 s) head=524288000 forventet=524288000 sha-lokal=9d8446ef…1319 sha-via-signert-GET=9d8446ef…1319 sha-boto3=9d8446ef…1319 PASS
utløpt signert adresse: 403 (forventer 403)
manipulert signatur: 403 (forventer 403)
signert GET med annen nøkkel enn signert: 403 (forventer 403)
```
Store filer gikk som signert PUT med curl til nøkkelen `stor/lyd æøå <n> MB.wav`.

## Ikke dekket
- Hetzner selv. Avvik i Hetzners S3-dialekt sees først ved utsetting.
- Cellens egne veier (`presignUpload`, `confirmUpload`, tilgang, måling). De dekkes av enhetstestene i PR #290 i CI.
- test.lagring.maaling mot tjenestens bruksrapport.

## Opprydding
Container, image (SeaweedFS og swift:6.1-noble), testdata og byggekatalog er slettet etter kjøringen. Se `docker ps -a` og `docker images` i loggen under.
