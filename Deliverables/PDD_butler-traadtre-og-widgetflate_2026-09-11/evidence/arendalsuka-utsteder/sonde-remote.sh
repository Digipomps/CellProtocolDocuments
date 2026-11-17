set -u
echo "vert: $(hostname)  bruker: $(id -un)  tid: $(date -u +%FT%TZ)"
for C in cellscaffold-app-1 cellscaffold-production-app-1; do
  echo
  echo "== $C"
  if ! docker inspect "$C" >/dev/null 2>&1; then echo "   containeren finnes ikke"; continue; fi
  echo "   -- mounts (Type | Source -> Destination):"
  docker inspect "$C" --format '{{range .Mounts}}      {{.Type}} | {{.Source}} -> {{.Destination}}
{{end}}'
  echo "   -- SQLITE_DATABASE_PATH i containeren:"
  docker inspect "$C" --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^SQLITE_DATABASE_PATH=/      /p'
  echo "   -- andre db-relaterte env:"
  docker inspect "$C" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -iE '^(DATABASE|SQLITE|CELLS|STORAGE|DATA)' | sed 's/^/      /'
  echo "   -- WorkingDir: $(docker inspect "$C" --format '{{.Config.WorkingDir}}')"
  echo "   -- db.sqlite sett INNENFRA:"
  docker exec "$C" sh -lc 'P="${SQLITE_DATABASE_PATH:-}"; [ -n "$P" ] && ls -la "$P" 2>&1; echo "--- ls /app/CellsContainer:"; ls -la /app/CellsContainer 2>&1 | head -25' 2>&1 | sed 's/^/      /'
done
echo
echo "== find db.sqlite (avgrenset, maxdepth 6)"
for R in /mnt/HC_Volume_104775511 /var/lib/haven /srv/haven /opt/haven /var/lib/docker/volumes; do
  [ -d "$R" ] || continue
  echo "   -- $R"
  find "$R" -maxdepth 6 -name 'db.sqlite' -type f 2>/dev/null | head -20 | sed 's/^/      /'
done
echo
echo "== docker volume ls"
docker volume ls 2>/dev/null | head -30 | sed 's/^/   /'
echo
echo "== /etc/haven/deploy-production.conf"
sed 's/^/   /' /etc/haven/deploy-production.conf 2>&1 | head -40
