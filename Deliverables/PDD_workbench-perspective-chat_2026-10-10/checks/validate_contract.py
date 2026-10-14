#!/usr/bin/env python3
"""Validate design examples only; no production API, authority or durability proof."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent

def validate(command,mount,contract):
    if not isinstance(command,dict) or not isinstance(mount,dict): return 'shape'
    if any(k not in command for k in contract['contracts']['command']['required']): return 'missing_field'
    if any(not isinstance(mount.get(k),str) or not mount[k] for k in contract['contracts']['mountContext']['required']): return 'mount'
    if command['schemaVersion']!=1: return 'schema'
    if type(command['expectedRevision']) is not int or command['expectedRevision']<0: return 'revision'
    if command['operation'] not in contract['operations']: return 'operation'
    if not isinstance(command['input'],dict): return 'input'
    if command['operation'] in contract['draftOperations']:
        draft=command['input'].get('draftSnapshot')
        if not isinstance(draft,dict) or any(k not in draft for k in ['mountInstanceID','fieldSequence','fieldKey','text']): return 'draft_required'
        if draft['mountInstanceID']!=mount['instanceID']: return 'draft_mount_mismatch'
        if type(draft['fieldSequence']) is not int or draft['fieldSequence']<0 or not isinstance(draft['text'],str): return 'draft_shape'
    if command['operation']=='savePackage':
        if type(command['input'].get('expectedPackageRevision')) is not int: return 'package_revision'
    return None

def main():
    spec=json.loads((ROOT/'contract/workbench-v1.json').read_text())
    fixtures=json.loads((ROOT/'contract/fixtures.json').read_text())
    for case in fixtures['cases']:
        actual=validate(case['command'],case['mountContext'],spec)
        assert actual==case['expectedError'], (case['name'],actual,case['expectedError'])
        assert case['valid']==(actual is None),case['name']
    terminal={'completed','denied','failed','cancelled'}
    transitions=spec['effectTransitions']
    assert all(not transitions[t] for t in terminal)
    assert 'dispatched' not in transitions['unknown'] and 'reserved' not in transitions['unknown']
    assert all(t in transitions for ts in transitions.values() for t in ts)
    print(json.dumps({'scope':'design-only','fixtureCases':len(fixtures['cases']),'status':'PASS','runtimeTests':'not run'},ensure_ascii=False))
if __name__=='__main__': main()
