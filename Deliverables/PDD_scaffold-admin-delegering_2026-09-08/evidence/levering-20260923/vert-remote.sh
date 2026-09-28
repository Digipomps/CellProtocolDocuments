set -u
dbsti(){ local c="$1" inner
  inner="$(docker inspect "$c" --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^SQLITE_DATABASE_PATH=//p' | head -1)"; [ -n "$inner" ] || inner=/app/CellsContainer/db.sqlite
  docker inspect "$c" --format '{{range .Mounts}}{{.Destination}}|{{.Source}}{{println}}{{end}}' | awk -F'|' -v inner="$inner" 'BEGIN{b=0} NF>=2{d=$1;s=$2; if(inner==d||index(inner,d "/")==1){ if(length(d)>b){b=length(d);u=s substr(inner,length(d)+1)} } } END{if(b>0)print u}'; }
for pair in "cellscaffold-app-1 8081" "cellscaffold-production-app-1 8084"; do
  set -- $pair; C=$1; PORT=$2
  echo "== $C"
  echo -n "  ready: "; timeout 20 curl -fsS "http://127.0.0.1:$PORT/health/ready" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("status"), "| advarsler:", d.get("runtimeAdvisories"))' 2>&1
  echo -n "  build: "; timeout 20 curl -fsS "http://127.0.0.1:$PORT/health/build" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("app_revision"))' 2>&1
  DB="$(dbsti "$C")"
  timeout 60 python3 - "$DB" <<'PY'
import sqlite3, sys
c = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
cols = [r[1] for r in c.execute("pragma table_info(fido_users)")]
idcol = "identity_id" if "identity_id" in cols else None
print("  fido_users-kolonner med id:", [x for x in cols if "id" in x.lower()])
q = "select id, username%s from fido_users where lower(username) in ('kjetil2','vegar','kjetil') or upper(id)='C8C99783-8522-40DE-A427-03E409090587'" % ((", " + idcol) if idcol else "")
for r in c.execute(q):
    print("  bruker:", " | ".join(str(x) for x in r))
PY
done
echo "== provisjoneringsskript paa verten?"
ls -la /usr/local/sbin 2>/dev/null | grep -i provision; ls -la /home/ops 2>/dev/null | grep -i provision | head
