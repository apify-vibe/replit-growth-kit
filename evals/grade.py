#!/usr/bin/env python3
"""Mechanical grader for evals/acceptance.md gates G3-G7 (G1, G2, G8 are read by hand).

Usage: python3 evals/grade.py evals/runs/<round>
Never trusts the subject's own claims: every run ID is re-read from the Apify API and sampled
output rows are checked against the raw dataset of the run they cite.
"""
import csv, json, os, random, re, sys, urllib.request, yaml
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = next(l.split('=', 1)[1].strip().strip('"\'') for l in open(os.path.expanduser('~/.claude/.env')) if l.startswith('APIFY_TOKEN='))
H = {'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'apify-replit-growth-kit/grader'}

def api(path):
    with urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2' + path, headers=H), timeout=60) as r:
        return json.load(r)

DELIVERABLES = {
    'open-web-lead-engine': (['leads.csv', 'review_needed_leads.csv', 'excluded_leads.csv', 'run_metadata.json'], 'leads.csv', 10),
    'demand-signal-scan': (['demand-signals.md', 'signals.csv'], 'signals.csv', 10),
    'competitor-teardown': (['competitor-teardown.md', 'pricing-comparison.csv', 'competitor-reviews.csv', 'competitor-signals.csv'], 'competitor-reviews.csv', 3),
    'creator-shortlist': (['creator-shortlist.md', 'creator-shortlist.csv'], 'creator-shortlist.csv', 8),
}
PROV_URL = ('source_url', 'url', 'profile_url')
PROV_RUN = ('source_run_id',)

def ts(s):
    s = s.strip().replace('Z', '+00:00')
    try: return datetime.fromisoformat(s)
    except ValueError: return None

def gate_times(path):
    if not os.path.exists(path): return []
    out = []
    for m in re.finditer(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?', open(path).read()):
        t = ts(m.group(0) if ('Z' in m.group(0) or '+' in m.group(0)[19:] or '-' in m.group(0)[19:]) else m.group(0) + '+00:00')
        if t: out.append(t)
    return sorted(out)

def read_csv(p):
    with open(p, newline='') as f: return list(csv.DictReader(f))

def grade(case, rdir):
    cdir = os.path.join(rdir, case['id']); skill = case['skill']; fit = case['fit']
    res = {'id': case['id'], 'skill': skill, 'fit': fit, 'notes': []}
    files, main_csv, min_rows = DELIVERABLES[skill]
    missing = [f for f in files if not os.path.exists(os.path.join(cdir, f))]
    res['files_missing'] = missing
    runs = json.load(open(os.path.join(cdir, 'runs.json'))) if os.path.exists(os.path.join(cdir, 'runs.json')) else []
    gates = gate_times(os.path.join(cdir, 'gates.log'))
    verified, cost, ungated, ua_ok, datasets = [], 0.0, [], 0, {}
    for r in runs:
        rid = r.get('runId') or r.get('id')
        if not rid: continue
        try: d = api(f'/actor-runs/{rid}')['data']
        except Exception as e: res['notes'].append(f'run {rid} not found: {e}'); continue
        u = d.get('usageTotalUsd') or 0; cost += u
        ua = (d.get('meta') or {}).get('userAgent') or ''
        if 'apify-replit-growth-kit' in ua: ua_ok += 1
        st = ts(d['startedAt'])
        if not any(g <= st for g in gates): ungated.append(rid)
        verified.append({'run': rid, 'status': d['status'], 'usd': round(u, 4), 'ua': ua[:60]})
        datasets[rid] = d.get('defaultDatasetId')
    res.update(runs_verified=len(verified), runs_listed=len(runs), cost_usd=round(cost, 4), ungated_runs=ungated,
               ua_attributed=f'{ua_ok}/{len(verified)}', runs=verified)
    # G2 mechanical part: bad-fit cases must have zero collection runs (one probe allowed for demand)
    if fit == 'bad':
        allowed = 1 if skill == 'demand-signal-scan' else 0
        res['G2_runs_ok'] = len(verified) <= allowed
    # G5/G6 on the main CSV
    p = os.path.join(cdir, main_csv); rows = []
    if os.path.exists(p):
        try: rows = read_csv(p)
        except Exception as e: res['notes'].append(f'csv parse error: {e}')
    if skill == 'creator-shortlist': rows = [r for r in rows if (r.get('status') or 'shortlisted') == 'shortlisted']
    res['main_rows'] = len(rows)
    if fit != 'bad': res['G6_rows_ok'] = len(rows) >= min_rows
    if rows:
        cols = rows[0].keys()
        urlc = next((c for c in PROV_URL if c in cols), None); runc = next((c for c in PROV_RUN if c in cols), None)
        res['G5_prov'] = {'url_col': urlc, 'run_col': runc,
                          'rows_missing_url': sum(1 for r in rows if urlc and not r[urlc].strip()) if urlc else len(rows),
                          'rows_missing_run': sum(1 for r in rows if runc and not r[runc].strip()) if runc else len(rows)}
        # G4: sample rows, check a distinctive value appears in the cited run's dataset
        random.seed(7); sample = random.sample(rows, min(10, len(rows))); hits = 0; cache = {}
        for r in sample:
            # A row filled from several runs (lead engine step 6) cites them all: "a; b" (also "+" or ",")
            rids = [x for x in re.split(r'[;,+\s]+', (r.get(runc) or '') if runc else '') if x]
            blob = ''
            for rid in rids:
                ds = datasets.get(rid)
                if not ds:
                    try: ds = api(f'/actor-runs/{rid}')['data']['defaultDatasetId']
                    except Exception: ds = None
                if not ds: continue
                if ds not in cache:
                    try: cache[ds] = json.dumps(api(f'/datasets/{ds}/items?clean=1&limit=5000')).lower()
                    except Exception: cache[ds] = ''
                blob += cache[ds]
            if not blob: continue
            probes = [r.get(k, '') for k in ('email', 'contact_email', 'url', 'source_url', 'profile_url', 'handle', 'quote', 'text', 'company_domain', 'title')]
            probes = [v.strip().lower() for v in probes if v and len(v.strip()) >= 6]
            if any((v[:80] in blob) or (v.split('?')[0].rstrip('/')[-40:] in blob) for v in probes): hits += 1
        res['G4_sample_traced'] = f'{hits}/{len(sample)}'
    return res

def main(rdir):
    cases = yaml.safe_load(open(os.path.join(ROOT, 'scenarios.yaml')))['cases']
    out = [grade(c, rdir) for c in cases if os.path.isdir(os.path.join(rdir, c['id']))]
    json.dump(out, open(os.path.join(rdir, 'grades-mechanical.json'), 'w'), indent=2)
    print(f"{'case':30} {'files':8} {'runs':6} {'cost':8} {'ungated':8} {'UA':6} {'rows':5} {'G4':6} {'G5 miss url/run':16} G2/G6")
    for r in out:
        g5 = r.get('G5_prov') or {}
        print(f"{r['id']:30} {('ok' if not r['files_missing'] else 'MISS'+str(len(r['files_missing']))):8} {r['runs_verified']:>2}/{r['runs_listed']:<3} {r['cost_usd']:<8} {len(r['ungated_runs']):<8} {r['ua_attributed']:6} {r.get('main_rows',0):<5} {r.get('G4_sample_traced','-'):6} {str(g5.get('rows_missing_url','-'))+'/'+str(g5.get('rows_missing_run','-')):16} {r.get('G2_runs_ok', r.get('G6_rows_ok'))}")
    print('total cost', round(sum(r['cost_usd'] for r in out), 4))

if __name__ == '__main__':
    main(sys.argv[1])
