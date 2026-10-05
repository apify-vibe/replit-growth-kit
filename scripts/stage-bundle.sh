#!/bin/bash
# Package the four skills for sharing and for Replit.
#   1. ~/Desktop/apify-growth-kit-skills-v1.2.zip   (share with Replit / Horacio)
#   2. Apify key-value store "replit-growth-kit-skills" (wg0mG9VcKHRQ9d3Py), records
#      skills.tgz + SHA256SUMS, readable anonymously by store ID, so a Repl can install
#      the skills without GitHub access.
# Token: APIFY_TOKEN parsed from ~/.claude/.env (never sourced, never printed).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS="open-web-lead-engine demand-signal-scan competitor-teardown creator-shortlist"
WORK="$(mktemp -d)"
cd "$ROOT/skills"
for s in $SKILLS; do npx --yes skills-ref validate "$s" >/dev/null; done
ZIP="$HOME/Desktop/apify-growth-kit-skills-v1.2.zip"
zip -r -X -q "$WORK/skills.zip" $SKILLS -x '*.DS_Store'
mv "$WORK/skills.zip" "$ZIP"
COPYFILE_DISABLE=1 tar -czf "$WORK/skills.tgz" $SKILLS
find $SKILLS -type f | sort | xargs shasum -a 256 > "$WORK/SHA256SUMS"
APIFY_TOKEN="$(grep -E '^APIFY_TOKEN=' "$HOME/.claude/.env" | head -1 | cut -d= -f2- | tr -d "\"' ")"
export APIFY_TOKEN WORK
python3 - <<'PY'
import hashlib, json, os, urllib.request
tok, work = os.environ["APIFY_TOKEN"], os.environ["WORK"]
H = {"Authorization": "Bearer " + tok, "User-Agent": "apify-replit-growth-kit/bundle"}
def call(method, path, data=None, ct=None):
    h = dict(H, **({"Content-Type": ct} if ct else {}))
    req = urllib.request.Request("https://api.apify.com/v2" + path, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
        return json.loads(b) if b else {}
sid = call("POST", "/key-value-stores?name=replit-growth-kit-skills")["data"]["id"]
for name, ct in [("skills.tgz", "application/gzip"), ("SHA256SUMS", "text/plain")]:
    call("PUT", f"/key-value-stores/{sid}/records/{name}", open(f"{work}/{name}", "rb").read(), ct)
call("PUT", f"/key-value-stores/{sid}", json.dumps({"generalAccess": "ANYONE_WITH_ID_CAN_READ"}).encode(), "application/json")
anon = urllib.request.urlopen(f"https://api.apify.com/v2/key-value-stores/{sid}/records/skills.tgz", timeout=60).read()
ok = hashlib.sha256(anon).hexdigest() == hashlib.sha256(open(f"{work}/skills.tgz", "rb").read()).hexdigest()
print(f"store {sid}: anonymous fetch matches local bundle: {ok}")
print(f"install URL: https://api.apify.com/v2/key-value-stores/{sid}/records/skills.tgz")
print(f"checksums:   https://api.apify.com/v2/key-value-stores/{sid}/records/SHA256SUMS")
PY
echo "zip: $ZIP"
head -1 "$WORK/SHA256SUMS"
