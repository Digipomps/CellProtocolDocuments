#!/usr/bin/env python3
"""Read checked-in fixture inputs, run actual Swift engine, compare binary floats."""
import argparse, json, pathlib, subprocess
from study import Engine, bits, json_file, generate
ROOT=pathlib.Path(__file__).resolve().parent

def check(data,out):
    en=Engine()
    for e in data['events']:en.apply(e)
    got={(e['fromNode']['id'],e['relationType'],e['toNode']['id']):e for e in out['edges']}
    assert got.keys()==en.edges.keys(),('keys',got.keys(),en.edges.keys())
    count=0
    for k,e in en.edges.items():
        for field,swift in [('w','weightStored'),('last','lastReinforcedAt')]:
            assert bits(e[field])==bits(got[k][swift]),(k,field,e[field],got[k][swift]);count+=1
        assert e['profile']==got[k]['decayProfileId'] and e['version']==got[k]['decayParamsVersion']
    for q,scores in zip(data['queries'],out['scores']):
        raw=en.score(q['snapshot'],q['at']);assert len(raw)==len(scores)
        for s in scores:
            r=raw[s['purposeId']];v=s['explain']['rawScore']
            assert bits(r)==bits(v),(q,s['purposeId'],r,v,bits(r),bits(v));count+=1
    return count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--oracle',required=True);ap.add_argument('--fixtures',type=pathlib.Path,default=ROOT/'oracle'/'fixtures');ap.add_argument('--out',type=pathlib.Path,default=ROOT/'resultater'/'swift_parity.json');args=ap.parse_args()
    results=[]
    for f in sorted(args.fixtures.glob('*.input.json')):
        data=json.loads(f.read_text());output=subprocess.check_output([args.oracle],input=json.dumps(data).encode());out=json.loads(output)
        if f.name.startswith(('old_','mixed_old')):
            expected=json.loads(f.with_name(f.name.replace('.input.','.output.')).read_text())
            assert out['edges']==expected['edges'], f.name
            results.append(dict(fixture=f.name,migration_original_output_equal=True,numeric_bit_checks=0,weights=[e['weightStored'] for e in out['edges']]))
            continue
        count=check(data,out);results.append(dict(fixture=f.name,numeric_bit_checks=count,source_replay_equals_arrival=out['replayEqual'],journal_restore_equals_arrival=out['restoreEqual'],weight_only_equals_arrival=out['weightOnlyEqual']))
    # Multi-episode baseline parity in each synthetic scenario; full matrix stays in Python.
    for scenario in ['sparse','dense','drift','preference_change','always_context','mixed']:
        data=generate(scenario,20,0);events=data['events'][:60];t=events[-1]['emittedAt']
        queries=[dict(at=t,snapshot=q['snapshot']) for q in data['queries'][:6]]
        test=dict(events=events,queries=queries)
        out=json.loads(subprocess.check_output([args.oracle],input=json.dumps(test).encode()))
        results.append(dict(fixture='matrix-prefix-'+scenario,numeric_bit_checks=check(test,out),source_replay_equals_arrival=out['replayEqual'],journal_restore_equals_arrival=out['restoreEqual']))
    json_file(args.out,dict(fixtures=results,total_bit_checks=sum(r['numeric_bit_checks'] for r in results),all_numeric_checks_pass=True))
    print('Swift baseline parity:',len(results),'fixtures;',sum(r['numeric_bit_checks'] for r in results),'identical binary floats')
if __name__=='__main__':main()
