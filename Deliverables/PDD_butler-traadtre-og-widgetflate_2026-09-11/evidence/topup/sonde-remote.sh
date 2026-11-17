set -u
ID_UP="D03228B6-4B53-4F8D-83CB-2E326DF63131"
dbsti(){ # container -> db-sti paa verten (samme logikk som rettet db_for)
  local c="$1" inner
  inner="$(docker inspect "$c" --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^SQLITE_DATABASE_PATH=//p' | head -1)"
  [ -n "$inner" ] || inner=/app/CellsContainer/db.sqlite
  docker inspect "$c" --format '{{range .Mounts}}{{.Destination}}|{{.Source}}{{println}}{{end}}' | awk -F'|' -v inner="$inner" '
    BEGIN{b=0} NF>=2{d=$1;s=$2; if(inner==d||index(inner,d "/")==1){ if(length(d)>b){b=length(d);u=s substr(inner,length(d)+1)} } } END{if(b>0)print u}'
}
for C in cellscaffold-app-1 cellscaffold-production-app-1; do
  echo; echo "################ $C"
  DB="$(dbsti "$C")"; echo "db: $DB"
  [ -f "$DB" ] || { echo "(fant ikke db)"; continue; }
  timeout 60 python3 - "$DB" "$ID_UP" <<'PY'
import sqlite3, sys, json
db, idu = sys.argv[1], sys.argv[2]
c = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
c.row_factory = sqlite3.Row
tabs = [r[0] for r in c.execute("select name from sqlite_master where type='table'")]
rel = [t for t in tabs if any(k in t.lower() for k in ("fund","topup","top_up","audit","ledger","prepaid","wallet","balance"))]
print("relevante tabeller:", rel)
def cols(t): return [r[1] for r in c.execute("pragma table_info('%s')" % t)]
# finn raden: id kan vaere tekst (store/smaa) eller blob
hits = []
for t in rel:
    cs = cols(t)
    for col in cs:
        try:
            q = "select * from '%s' where upper(cast(%s as text))=? or hex(%s)=?" % (t, col, col)
            rows = c.execute(q, (idu, idu.replace("-",""))).fetchall()
        except Exception as e:
            continue
        for r in rows:
            hits.append((t, col, dict(r)))
for t, col, r in hits:
    print("\n=== treff i %s.%s" % (t, col))
    for k, v in r.items():
        if isinstance(v, bytes): v = v.hex()
        s = str(v)
        print("  %s = %s" % (k, s[:1500]))
# de siste top-up-hendelsene uansett id, for kontekst
for t in rel:
    cs = cols(t)
    if "action" in cs:
        order = "created_at" if "created_at" in cs else ("timestamp" if "timestamp" in cs else "rowid")
        print("\n=== siste 12 TOPUP-hendelser i %s (sortert paa %s)" % (t, order))
        for r in c.execute("select * from '%s' where action like 'TOPUP%%' order by %s desc limit 12" % (t, order)):
            d = dict(r)
            for k in list(d):
                if isinstance(d[k], bytes): d[k] = d[k].hex()
            print("  " + json.dumps(d, ensure_ascii=False, default=str)[:1500])
PY
done
echo; echo "################ containere (ogsaa stoppede/omdoepte)"
docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.CreatedAt}}' | grep -i cellscaffold | head -20
echo; echo "################ approve-kall i containerlogger"
for C in $(docker ps -a --format '{{.Names}}' | grep -i cellscaffold); do
  N="$(timeout 30 docker logs "$C" 2>&1 | grep -ciE 'funding-requests/.*approve|TOPUP_APPLY_FAILED|issuePrepaid')"
  [ "${N:-0}" -gt 0 ] || continue
  echo "== $C ($N linjer)"
  timeout 30 docker logs --timestamps "$C" 2>&1 | grep -iE -B3 -A12 'funding-requests/.*approve|TOPUP_APPLY_FAILED' | tail -80
done
