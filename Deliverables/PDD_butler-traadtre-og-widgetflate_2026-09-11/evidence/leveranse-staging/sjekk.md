Noekkel: `id_ed25519_hetzner`. Bruker: `ops@89.167.90.101`, BatchMode.

## Hva ops faktisk har lov til

`sudo -n -l` → exit 0.

```text
Matching Defaults entries for ops on ubuntu-16gb-hel1-1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ops may run the following commands on ubuntu-16gb-hel1-1:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/local/sbin/haven-admin-access
    (root) NOPASSWD: /usr/local/sbin/haven-deploy
    (root) NOPASSWD: /usr/local/sbin/haven-deploy-doctor
    (root) NOPASSWD: /usr/local/sbin/haven-ghcr-prefetch
    (root) NOPASSWD: /usr/local/sbin/haven-ghcr-prefetch-production
    (root) NOPASSWD: /usr/local/sbin/haven-manifest-provision
    (root) NOPASSWD: /usr/bin/systemctl start haven-deploy@*
    (root) NOPASSWD: /usr/bin/systemctl status haven-deploy@*
    (root) NOPASSWD: /usr/bin/systemctl is-active haven-deploy@*
    (root) NOPASSWD: /usr/bin/journalctl -u haven-deploy@*
```

## Diskvakten (prefetch krever plass)

`df -h /var/lib/docker / /mnt/disk1 2>/dev/null` → exit 0.

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdc        196G  103G   84G  55% /var/lib/docker
/dev/sda1       150G  105G   40G  73% /
/dev/sda1       150G  105G   40G  73% /
```

## Containere som kjoerer

`docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'` → exit 0.

```text
palazzo-staging-app  ghcr.io/dimy-io/palazzoscaffold:sha-0b74f9051cfe38c88c282277da2575e26624fa26  Up 8 hours (healthy)
cellscaffold-production-app-1  cellscaffold-production-candidate:sha-e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8  Up 4 days
cellscaffold-app-1  cellscaffold-staging-local:sha-e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8  Up 4 days
amici  amici:latest  Up 2 weeks
buildx_buildkit_haven-production-oci-import-v10  moby/buildkit:buildx-stable-1  Up 4 weeks
cellscaffold-admin-scaffold-1  cellscaffold-admin-release:f76de5a-9577e532  Up 13 hours (healthy)
admin-monitoring-prometheus-1  69f524141883  Up 5 weeks
admin-monitoring-alertmanager-1  51a825c2a40a  Up 5 weeks
admin-monitoring-blackbox-exporter-1  e753ff9f3fc4  Up 5 weeks
admin-monitoring-node-exporter-1  0f422f62c15f  Up 5 weeks
deploy-palazzo-concierge-1  pypalazzo-concierge-scaffold:staging  Up 5 weeks
admin-scaffold-production-app-1  127.0.0.1:5000/digipomps/cellscaffold-admin  Up 11 days (healthy)
haven-production-registry  46faa9a1ae68  Up 5 weeks
emergentuniverse-rag-api-1  docker-rag_innovasjon_api  Up 5 weeks
emergentuniverse-rag-db-1  pgvector/pgvector:pg16  Up 5 weeks (healthy)
cellscaffold-swarm-1  cellscaffold-swarm:latest  Up 5 weeks
spatial-registry-staging-spatial-registry-app-1  spatial-registry-scaffold:staging  Up 5 weeks
spatial-registry-staging-postgis-staging-1  postgis/postgis:17-3.5  Up 5 weeks (healthy)
docker-rag_innovasjon_api-1  docker-rag_innovasjon_api  Up 5 weeks
docker-rag_dimy_api-1  docker-rag_dimy_api  Up 5 weeks
docker-rag_innovasjon_db-1  pgvector/pgvector:pg16  Up 5 weeks (healthy)
docker-rag_dimy_db-1  pgvector/pgvector:pg16  Up 5 weeks (healthy)
```

## Staging /health/build (fra verten)

`curl -fsS --max-time 10 http://127.0.0.1:8081/health/build` → exit 0.

```text
{"build_timestamp":"2026-09-18T12:21:55Z","dimymicropayments_revision":"cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","cellprotocol_revision":"533b42d5dc25cf1453cbe5ad08f523d47d5d32e9","app_revision":"e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8","environment":"staging","dimymint_revision":"ffdb0da85fc45be16926bfa5d335b247205f1b79","status":"ok"}```

## Produksjon /health/build (fra verten, bare lest)

`curl -fsS --max-time 10 http://127.0.0.1:8084/health/build` → exit 0.

```text
{"status":"ok","build_timestamp":"2026-09-18T12:21:55Z","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","environment":"production","cellprotocol_revision":"533b42d5dc25cf1453cbe5ad08f523d47d5d32e9","dimymicropayments_revision":"cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0","dimymint_revision":"ffdb0da85fc45be16926bfa5d335b247205f1b79","app_revision":"e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8"}```

## Offentlig, sett utenfra

- `https://staging.haven.digipomps.org/health/build`: `{"package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","dimymicropayments_revision":"cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0","app_revision":"e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8","cellprotocol_revision":"533b42d5dc25cf1453cbe5ad08f523d47d5d3`
- `https://haven.digipomps.org/health/build`: `{"dimymint_revision":"ffdb0da85fc45be16926bfa5d335b247205f1b79","app_revision":"e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8","build_timestamp":"2026-09-18T12:21:55Z","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","dimymicropayments_revision":"`

Merk: prod leses bare. Ingenting her endrer noe, og prod skal ikke roeres foer Kjetil sier fra.
