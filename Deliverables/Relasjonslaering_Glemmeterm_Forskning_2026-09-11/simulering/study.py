#!/usr/bin/env python3
"""Offline research harness. No production imports or writes; Python stdlib only.
Numeric baseline is checked against a separately compiled unmodified Swift engine.
All sums in learning/scoring use explicit left folds (Swift Double semantics).
"""
import argparse, copy, csv, gzip, hashlib, io, json, math, pathlib, random, statistics, struct, sys
from collections import defaultdict, deque
ROOT = pathlib.Path(__file__).resolve().parent
SCENARIOS = ['sparse', 'dense', 'drift', 'preference_change', 'always_context', 'mixed']
MODES = ['baseline', 'hybrid_raw_005', 'hybrid_raw_02', 'hybrid_raw_08', 'hybrid_clamp', 'oja_raw', 'centered_oja', 'budget']
RATE = {'hybrid_raw_005': .005, 'hybrid_raw_02': .02, 'hybrid_raw_08': .08, 'hybrid_clamp': .02}
TYPES = {'purposeInterest':'interest', 'purposeEntity':'entityRepresentation', 'purposeContextBlock':'contextBlock', 'purposePurpose':'purpose'}
FIELDS = ['activeInterestRefs','passiveInterestRefs','activeEntityRefs','passiveEntityRefs']
def clamp(x): return min(1.0, max(0.0, x))
def fold(xs):
    total = 0.0
    for x in xs: total += x
    return total
def norm(xs): return math.sqrt(fold(x*x for x in xs))
def bits(x): return struct.pack('>d', x).hex()
def canonical(x): return json.dumps(x, sort_keys=True, separators=(',',':'), ensure_ascii=False, allow_nan=False)
def digest(x): return hashlib.sha256(canonical(x).encode()).hexdigest()
def sign(x): return (x>0)-(x<0)
def soft(x): return x/(1.0+x)
def rank(values): return sorted(values, key=lambda p:(-values[p], p))
def tau_b(a,b):
    keys=sorted(a); pairs=[(sign(a[p]-a[q]),sign(b[p]-b[q])) for j,p in enumerate(keys) for q in keys[j+1:]]
    den=math.sqrt(fold(x*x for x,y in pairs)*fold(y*y for x,y in pairs))
    return fold(x*y for x,y in pairs)/den if den else None
def tau_total(a,b):
    ar={p:i for i,p in enumerate(a)};br={p:i for i,p in enumerate(b)}
    k=sorted(ar);return fold(sign(ar[p]-ar[q])*sign(br[p]-br[q]) for j,p in enumerate(k) for q in k[j+1:])/(len(k)*(len(k)-1)/2)
def noa(delta, params=None):
    p=params or dict(t1Seconds=604800.0,t2Seconds=2592000.0,k1=1.2,k2=.6,rMin=.05)
    d=max(0.,delta); t1=p['t1Seconds']; t2=p['t2Seconds']
    k1=max(1.,p['k1']*t1); k2=max(1.,p['k2']*t2)
    s1=1/(1+math.exp((d-t1)/k1)); s2=1/(1+math.exp((d-t2)/k2))
    b1=1/(1+math.exp(-t1/k1));b2=1/(1+math.exp(-t2/k2));base=max(1e-9,b1*b2)
    shape=(s1*s2)/base
    return clamp(p['rMin']+(1-p['rMin'])*shape)
def env(kind,payload): return dict(eventType=kind,schemaVersion='1.0',emittedAt=payload.get('timestamp',payload.get('emittedAt')),payload=payload)
def snap(**kw): return dict(activeInterestRefs=[],passiveInterestRefs=[],activeEntityRefs=[],passiveEntityRefs=[],activeContextBlocks=[])|kw
def life(id,t,status,p='P',**kw): return env('purposeLifecycle',dict(eventId=id,timestamp=t,status=status,purposeId=p,metadata={})|snap()|kw)
def pref(id,t,p,target,w=.6,rel='purposeInterest'): return env('explicitPreference',dict(eventId=id,timestamp=t,purposeId=p,relationType=rel,targetNode=dict(type=TYPES[rel],id=target),preferenceWeight=w,metadata={}))
def ordered(events): return sorted(events,key=lambda e:(e['emittedAt'],e['eventType'],e['payload']['eventId'],canonical(e['payload'])))
def signal_id(b): return b['domain']+':'+b['blockId']
def traces(snapshot):
    result={}
    for field,rel,x in [('activeInterestRefs','purposeInterest',1.),('passiveInterestRefs','purposeInterest',.3),('activeEntityRefs','purposeEntity',1.),('passiveEntityRefs','purposeEntity',.3)]:
        for ref in sorted(snapshot.get(field,[])):
            if ref: result[(rel,ref)]=max(result.get((rel,ref),0),x)
    for b in snapshot.get('activeContextBlocks',[]):
        if b['confidence']>=.6: result[('purposeContextBlock',signal_id(b))]=clamp(.5*b['confidence'])
    return result

class Engine:
    def __init__(self,mode='baseline',cutover=0,only_eligible=False):
        self.mode=mode;self.cutover=cutover;self.only_eligible=only_eligible
        self.edges={};self.sessions={};self.context={};self.seen=set();self.updates=[];self.history=defaultdict(lambda:deque(maxlen=32))
        self.policies={'noa':[dict(profileId='noa',version=1,effectiveFromTimestamp=0,kind='noaDoubleSigmoid')]}
    def policy(self,profile,t,version=1):
        ps=sorted(self.policies.get(profile,[]),key=lambda p:(p['effectiveFromTimestamp'],p['version']))
        return next((p for p in reversed(ps) if p['effectiveFromTimestamp']<=t),None) or next((p for p in ps if p['version']==version),None) or (ps[-1] if ps else dict(profileId='noa',version=1,effectiveFromTimestamp=0,kind='noaDoubleSigmoid'))
    def new_edge(self,t):
        p=self.policy('noa',t)
        return dict(w=.1,last=t,profile=p['profileId'],version=p['version'])
    def snapshot(self):
        return dict(edges=[dict(purpose=k[0],relation=k[1],target=k[2],**v) for k,v in sorted(self.edges.items())],history={p:[sorted((list(k),v) for k,v in x.items()) for x in h] for p,h in sorted(self.history.items())})
    def score(self,s,t):
        x=traces(s); raw={p:0. for p,r,i in self.edges}
        for (p,r,i),edge in sorted(self.edges.items()):
            e=x.get((r,i),0.)
            if e<=0:continue
            pol=self.policy(edge['profile'],t,edge['version'])
            retention=1. if pol['kind']=='none' else noa(t-edge['last'],pol.get('noaParameters'))
            raw[p]+=clamp(edge['w']*retention)*e
        return raw
    def update(self,key,old,new,t,x,event,terms):
        edge=copy.copy(old);edge['w']=clamp(new)
        # Baseline also refreshes on failures. Competition alone is not reinforcement.
        if x>0:
            edge['last']=t;p=self.policy('noa',t);edge['profile']=p['profileId'];edge['version']=p['version']
        self.edges[key]=edge
        self.updates.append(dict(source=event,key=list(key),before=old['w'],after=edge['w'],last=edge['last'],profile=edge['profile'],version=edge['version'],eligibility=x,**terms))
    def apply(self,e):
        p=e['payload'];kind=e['eventType'];t=e['emittedAt'];eid=p['eventId'];identity=(kind,eid)
        if identity in self.seen:return
        self.seen.add(identity)
        if kind=='contextTransition':
            self.context[p['domain']]=dict(domain=p['domain'],blockId=p['toBlockId'],confidence=p['confidence'],metadata=p.get('metadata',{}));return
        if kind=='decayPolicyUpdated':
            pol=copy.deepcopy(p['policy']);xs=self.policies.setdefault(pol['profileId'],[])
            self.policies[pol['profileId']]=[v for v in xs if v['version']!=pol['version']]+[pol];return
        if kind=='explicitPreference':
            key=(p['purposeId'],p['relationType'],p['targetNode']['id']);old=self.edges.get(key,self.new_edge(t))
            self.update(key,old,p['preferenceWeight'],t,1.,eid,dict(kind='explicitPreference'));return
        if kind=='weightUpdate':
            edge=p['edge'];key=(edge['fromNode']['id'],edge['relationType'],edge['toNode']['id'])
            self.edges[key]=dict(w=clamp(p['newWeightStored']),last=edge['lastReinforcedAt'],profile=edge['decayProfileId'],version=edge['decayParamsVersion']);return
        assert kind=='purposeLifecycle'
        purpose=p['purposeId'];s=copy.deepcopy(p)
        if p['status']=='started':
            blocks={signal_id(b):b for b in s['activeContextBlocks']}
            blocks.update({signal_id(b):b for b in self.context.values()});s['activeContextBlocks']=list(blocks.values());self.sessions[purpose]=s;return
        start=self.sessions.pop(purpose,None)
        if start:
            for f in FIELDS:s[f]=sorted(set(start[f])|set(p[f]))
            blocks={signal_id(b):b for b in start['activeContextBlocks']};blocks.update({signal_id(b):b for b in p['activeContextBlocks']})
            s['activeContextBlocks']=list(blocks.values())
            if p.get('contextConfidence') is None:s['contextConfidence']=start.get('contextConfidence')
        blocks={signal_id(b):b for b in s['activeContextBlocks']};blocks.update({signal_id(b):b for b in self.context.values()});s['activeContextBlocks']=list(blocks.values())
        conf=s.get('contextConfidence');conf=1. if conf is None else conf
        if conf<.6:return
        x=traces(s);mode=self.mode if t>=self.cutover else 'baseline';success=p['status']=='succeeded'
        old={k:v.copy() for k,v in self.edges.items() if k[0]==purpose and k[1]!='purposePurpose'}
        for r,i in x:old.setdefault((purpose,r,i),self.new_edge(t))
        keys=sorted(old) if success and mode!='baseline' and not self.only_eligible else sorted((purpose,r,i) for r,i in x)
        y=fold(old[k]['w']*x.get(k[1:],0.) for k in sorted(old))
        z={k:x.get(k[1:],0.) for k in keys}
        if mode=='centered_oja':
            hist=self.history[purpose]
            for k in keys:z[k]-=fold(h.get(k[1:],0.) for h in hist)/len(hist) if hist else 0.
            y=fold(old[k]['w']*z[k] for k in keys)
        elif mode in ('hybrid_clamp','oja_clamp'):y=clamp(y)
        nexts={};deltas={}
        for k in keys:
            w=old[k]['w'];xi=x.get(k[1:],0.)
            gain=.08*xi*(1-w) if success else -.05*xi*w;forget=0.
            if success and mode in RATE:forget=RATE[mode]*y*y*w
            if success and mode in ('oja_raw','oja_clamp','centered_oja'):
                gain=.01*y*z[k];forget=.01*y*y*w
            nexts[k]=clamp(w+gain-forget);deltas[k]=(gain,forget)
        factor=1.
        if success and mode=='budget':factor=max(1.,norm(nexts.values()));nexts={k:v/factor for k,v in nexts.items()}
        for k in keys:
            gain,forget=deltas[k]
            self.update(k,old[k],nexts[k],t,x.get(k[1:],0.),eid,dict(kind=mode,y=y,gain=gain,forget=forget,budgetDivisor=factor,projectionResidual=nexts[k]-(old[k]['w']+gain-forget)))
        if success and mode=='centered_oja':self.history[purpose].append(x.copy())

def replay(events,mode='baseline',**kw):
    en=Engine(mode,**kw)
    for e in ordered(events):en.apply(e)
    return en

def gzip_json(path,value):
    with open(path,'wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz:gz.write((canonical(value)+'\n').encode())
def read_json(path):
    return json.loads(gzip.open(path,'rt').read() if str(path).endswith('.gz') else pathlib.Path(path).read_text())
def json_file(path,value):pathlib.Path(path).write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n')

def references():
    null=[.1]*6;positive=[.17200000000000001]*6
    ref=dict(saturation=dict(null_raw=fold(null),positive_raw=fold(positive),null=clamp(fold(null))==1,positive=clamp(fold(positive))==1),ranking=dict(null=rank({'A':2.,'B':1.}),positive=rank({'A':1.,'B':2.})),tau=dict(identical=tau_b({'A':1.,'B':2.},{'A':1.,'B':2.}),reversed=tau_b({'A':1.,'B':2.},{'A':2.,'B':1.}),all_ties=tau_b({'A':1.,'B':1.},{'A':1.,'B':1.})),norm=dict(null=norm([.6,.8]),positive=norm([.8,.8])),weight_change=dict(null=norm([0.,0.]),positive=norm([.072,0.])),bits=dict(null=bits(.1)==bits(.1),positive=bits(.1)==bits(math.nextafter(.1,1.))))
    ref['top_accuracy']=dict(null=statistics.mean(t=='B' for t in ['A']*10),positive=statistics.mean(t=='B' for t in ['B']*10))
    ref['positive_margin']=dict(null=sign(0.2-0.8),positive=sign(0.8-0.2))
    assert ref['top_accuracy']==dict(null=0,positive=1) and ref['positive_margin']==dict(null=-1,positive=1)
    ref['adaptation']=dict(no_switch=adaptation(['A']*20,'B',0),switch=adaptation(['A']*3+['B']*17,'B',0))
    assert ref['saturation']['null'] is False and ref['saturation']['positive'] is True
    assert ref['tau']['identical']==1 and ref['tau']['reversed']==-1 and ref['tau']['all_ties'] is None
    assert ref['norm']['null']==1 and ref['norm']['positive']>1 and ref['weight_change']['positive']>0
    assert ref['ranking']['null']!=ref['ranking']['positive'] and ref['bits']['null'] and not ref['bits']['positive']
    assert ref['adaptation']['switch']['first']==3 and ref['adaptation']['no_switch']['first'] is None
    return ref

def adaptation(tops,target,offset=90):
    after=tops[offset:];first=next((i for i,x in enumerate(after) if x==target),None)
    stable=next((i for i in range(max(0,len(after)-9)) if all(x==target for x in after[i:i+10])),None)
    return dict(first=first,stable=stable,observed=len(after),censored=stable is None)

def generate(scenario,n,seed):
    rng=random.Random(seed+1000*n+100000*SCENARIOS.index(scenario));events=[];queries=[]
    for step in range(180):
        t=step*3600.;p='ABC'[step%3];target='B' if step>=90 and scenario in ('drift','preference_change') else 'C'
        s=snap();begin=snap()
        for i in range(n):
            if scenario=='always_context' and i==n-1:
                s['activeContextBlocks'].append(dict(domain='time',blockId='always',confidence=1.,metadata={}));continue
            if scenario=='mixed' and i==n-1:
                c=rng.choice([.59,.6,.8,1.]);s['activeContextBlocks'].append(dict(domain='location',blockId='common',confidence=c,metadata={}));continue
            prob=1. if scenario=='dense' else (.13 if scenario in ('sparse','always_context') else .55)
            if scenario=='drift':prob=.85 if (i<n/2)==(step<90) else .1
            rel='Interest' if i%2==0 else 'Entity';v=rng.random();fid=f'f{i:02}'
            if v<prob:s[f'active{rel}Refs'].append(fid)
            elif v<prob+.12:s[f'passive{rel}Refs'].append(fid)
        # Exercise union: a subset appears only at start, same query contains the union.
        finish=copy.deepcopy(s)
        for f in FIELDS:
            begin[f]=s[f][::2];finish[f]=s[f][1::2]
        conf=.59 if scenario=='mixed' and step%17==0 else 1.
        if scenario=='preference_change' and step==90:events.append(pref('preference-switch',t-1,'B','f00',.6))
        events.append(life(f'{step:04}-start',t,'started',p,**begin,contextConfidence=conf))
        ok=rng.random() < (.9 if p==target else .3)
        events.append(life(f'{step:04}-end',t+30,'succeeded' if ok else 'failed',p,**finish))
        queries.append(dict(step=step,at=t+30,snapshot=s,target=target))
    return dict(scenario=scenario,n=n,seed=seed,events=events,queries=queries)

def simulate(data,mode):
    en=Engine(mode);groups=defaultdict(list)
    for e in ordered(data['events']):groups[e['emittedAt']].append(e)
    flat=ordered(data['events']);idx=0;hist=[];tops=[];raw_tops=[];sats=[];taus=[];rawtau=[];margins=[];changes=[];previous=None;previous_edges={};distort=[]
    for q in data['queries']:
        while idx<len(flat) and flat[idx]['emittedAt']<=q['at']:en.apply(flat[idx]);idx+=1
        actual=en.score(q['snapshot'],q['at']);actual_cl={p:clamp(v) for p,v in actual.items()}
        raw={p:actual.get(p,0.) for p in 'ABC'}
        cl={p:clamp(v) for p,v in raw.items()};sr={p:soft(v) for p,v in raw.items()}
        top=rank(actual_cl)[0] if actual_cl else None;rtop=rank(actual)[0] if actual else None;tops.append(top);raw_tops.append(rtop)
        sats.extend(v==1 for v in actual_cl.values());rawtau.append(tau_b(raw,cl));margins.append(raw[q['target']]-max(v for p,v in raw.items() if p!=q['target']))
        if previous:taus.append(tau_total(rank(previous),rank(cl)))
        previous=cl
        for j,p in enumerate('ABC'):
            for other in 'ABC'[j+1:]:
                a=sign(raw[p]-raw[other]);b=sign(sr[p]-sr[other]);c=sign(cl[p]-cl[other]);distort.append((a!=b,a!=c))
        current={k:v['w'] for k,v in en.edges.items()};change=norm(current.get(k,0)-previous_edges.get(k,0) for k in sorted(set(current)|set(previous_edges)));changes.append(change);previous_edges=current
        ns={p:norm(v['w'] for k,v in en.edges.items() if k[0]==p) for p in 'ABC'}
        hist.append(dict(step=q['step'],target=q['target'],candidate_count=len(actual),raw=raw,score=cl,soft=sr,norm=ns,weight_l2_change=change))
    again=replay(data['events'],mode)
    # These source logs have no conflicting equal-time IDs. Shuffle tests canonical order.
    shuffled=list(data['events']);random.Random(910).shuffle(shuffled);again2=replay(shuffled,mode)
    assert canonical(en.snapshot())==canonical(again.snapshot())==canonical(again2.snapshot())
    ev_edges={}
    for u in en.updates:ev_edges[tuple(u['key'])]=dict(w=u['after'],last=u['last'],profile=u['profile'],version=u['version'])
    assert ev_edges==en.edges # Edge projection only; centered history still needs lifecycle replay.
    assert all(math.isfinite(v['w']) and 0<=v['w']<=1 for v in en.edges.values())
    metrics=dict(scenario=data['scenario'],n=data['n'],seed=data['seed'],mode=mode,saturation=statistics.mean(sats),top_accuracy=statistics.mean(t==q['target'] for t,q in zip(tops,data['queries'])),raw_top_accuracy=statistics.mean(t==q['target'] for t,q in zip(raw_tops,data['queries'])),temporal_tau=statistics.mean(taus),raw_clamp_tau=statistics.mean(v for v in rawtau if v is not None) if any(v is not None for v in rawtau) else None,raw_clamp_tau_defined=sum(v is not None for v in rawtau),final_norm_mean=statistics.mean(hist[-1]['norm'].values()),max_norm=max(v for h in hist for v in h['norm'].values()),last30_weight_delta=statistics.mean(changes[-30:]),target_positive_margin_fraction=statistics.mean(m>0 for m in margins),soft_sign_changes=sum(a for a,b in distort),clamp_sign_changes=sum(b for a,b in distort),pair_count=len(distort),replay_bit_equal=True,edge_event_replay_equal=True,final_state_sha256=digest(en.snapshot()),updates=len(en.updates))
    if data['scenario'] in ('drift','preference_change'):
        metrics['adapt_clamp']=adaptation(tops,'B');metrics['adapt_raw']=adaptation(raw_tops,'B')
    return metrics,hist,en.snapshot()

def controls():
    rows=[]
    for n in [2,6,20]:
        events=[env('decayPolicyUpdated',dict(eventId='none',emittedAt=0.,policy=dict(profileId='noa',version=2,effectiveFromTimestamp=0.,kind='none')))]
        for j in range(1500):events.append(life(f'{j:06}',j+1.,'succeeded',activeInterestRefs=[f'i{i:02}' for i in range(n)]))
        for mode in MODES+['oja_clamp']:
            en=replay(events,mode);raw=en.score(snap(activeInterestRefs=[f'i{i:02}' for i in range(n)]),1500.)['P']
            rows.append(dict(n=n,mode=mode,raw=raw,score=clamp(raw),soft=soft(raw),norm=norm(v['w'] for v in en.edges.values()),min_weight=min(v['w'] for v in en.edges.values()),max_weight=max(v['w'] for v in en.edges.values())))
    e=[pref('seed-a',0.,'P','a',.6),pref('seed-b',0.,'P','b',.6),life('s',1.,'succeeded',activeInterestRefs=['b'])]
    ablation=[]
    for only in [False,True]:
        en=replay(e,'hybrid_raw_02',only_eligible=only);a=en.edges[('P','purposeInterest','a')]
        ablation.append(dict(only_eligible=only,absent_weight=a['w'],last=a['last'],effective_1s=a['w']*noa(1),effective_30d=a['w']*noa(30*86400),retention_30d=noa(30*86400),updates=en.updates[-2:]))
    # Independent feature stream: constant context versus two anti-correlated inputs.
    center=[]
    for mode in ['oja_raw','centered_oja','budget']:
        en=Engine(mode)
        for j in range(2000):en.apply(life(str(j),float(j),'succeeded',activeInterestRefs=['a' if j%2==0 else 'b'],activeContextBlocks=[dict(domain='time',blockId='always',confidence=1.,metadata={})]))
        center.append(dict(mode=mode,weights={k[2]:v['w'] for k,v in sorted(en.edges.items())},norm=norm(v['w'] for v in en.edges.values())))
    # Explicit preference is exact immediately but a subsequent budget step may reduce it.
    preference=[]
    for mode in MODES:
        en=Engine(mode)
        for i in range(6):en.apply(pref(f'p{i}',0.,'P',f'i{i}',.6))
        before=norm(v['w'] for v in en.edges.values());en.apply(life('s',1.,'succeeded',activeInterestRefs=['i0']))
        preference.append(dict(mode=mode,norm_after_preferences=before,norm_after_success=norm(v['w'] for v in en.edges.values()),unobserved_preference_weight=en.edges[('P','purposeInterest','i1')]['w']))
    return dict(steady_state=rows,absence_ablation=ablation,centering=center,explicit_preference=preference)

def main():
    source_hash=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,default=ROOT/'resultater');ap.add_argument('--quick',action='store_true');args=ap.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    json_file(out/'instrument_references.json',references())
    # All gates above have measured null and positive references before candidate execution.
    datasets=[generate(s,n,seed) for s in SCENARIOS for n in [2,6,20] for seed in range(1 if args.quick else 8)]
    gzip_json(out/'synthetic_logs.json.gz',datasets)
    results=[];histories=[];states=[]
    for j,data in enumerate(datasets):
        for mode in MODES:
            metrics,hist,state=simulate(data,mode);results.append(metrics)
            if data['seed']==0:histories.append(dict(scenario=data['scenario'],n=data['n'],mode=mode,history=hist))
            states.append(dict(scenario=data['scenario'],n=data['n'],seed=data['seed'],mode=mode,state=state))
        if j%24==0:print(f'processed {j+1}/{len(datasets)} logs',flush=True)
    json_file(out/'seed_metrics.json',results);gzip_json(out/'representative_histories.json.gz',histories);gzip_json(out/'final_states.json.gz',states)
    groups=defaultdict(list)
    for r in results:groups[(r['scenario'],r['n'],r['mode'])].append(r)
    summary=[]
    for (scenario,n,mode),rs in groups.items():
        row=dict(scenario=scenario,n=n,mode=mode,seeds=len(rs))
        for key in ['saturation','top_accuracy','raw_top_accuracy','temporal_tau','final_norm_mean','max_norm','last30_weight_delta','target_positive_margin_fraction']:
            vals=[r[key] for r in rs];row[key]=statistics.mean(vals);row[key+'_min']=min(vals);row[key+'_max']=max(vals)
        base=groups[(scenario,n,'baseline')]
        diffs=[r['raw_top_accuracy']-b['raw_top_accuracy'] for r,b in zip(rs,base)]
        row['raw_accuracy_win_loss_tie']=[sum(x>0 for x in diffs),sum(x<0 for x in diffs),sum(x==0 for x in diffs)]
        if scenario in ('drift','preference_change'):
            for scoring in ['raw','clamp']:
                vals=[r['adapt_'+scoring]['stable'] for r in rs];observed=[v for v in vals if v is not None]
                row['adapt_'+scoring+'_censored']=sum(v is None for v in vals);row['adapt_'+scoring+'_median_observed']=statistics.median(observed) if observed else None
        summary.append(row)
    json_file(out/'aggregate.json',summary);json_file(out/'controls.json',controls())
    assert source_hash==hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), 'Simulator changed during run'
    manifest=dict(schema='relational-study-artifacts-v1',python=sys.version,logs=len(datasets),candidate_runs=len(results),seed_count=1 if args.quick else 8,source_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),prereg_sha256=hashlib.sha256((ROOT.parent/'PREREGISTRERING.md').read_bytes()).hexdigest(),all_replays_equal=all(r['replay_bit_equal'] for r in results),total_soft_sign_changes=sum(r['soft_sign_changes'] for r in results),total_clamp_sign_changes=sum(r['clamp_sign_changes'] for r in results),total_comparisons=sum(r['pair_count'] for r in results),files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.name in {'aggregate.json','controls.json','final_states.json.gz','instrument_references.json','representative_histories.json.gz','seed_metrics.json','synthetic_logs.json.gz'}})
    json_file(out/'manifest.json',manifest);print(canonical(manifest))
if __name__=='__main__':main()
