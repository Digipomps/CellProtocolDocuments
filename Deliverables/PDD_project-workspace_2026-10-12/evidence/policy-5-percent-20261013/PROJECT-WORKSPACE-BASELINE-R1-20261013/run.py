"""One coordinated baseline of the G2 project workspace inputs; no product edits."""
from pathlib import Path
import datetime, hashlib, json, os, re, resource, subprocess, sys
sys.dont_write_bytecode = True
from workbench_xctest_receipt import validate_xctest
from command_control import run_owned_command, install_interrupt_handlers, deferred_cleanup_interruptions
import owned_process

HERE = Path(__file__).resolve().parent
H = Path.home()/'Build/Digipomps/HAVEN'
CS = Path.home()/'.codex/worktrees/project-workspace-20261013/CellScaffold'
JOB = 'project-workspace-baseline-r1-20261013'
M = json.loads((HERE/'manifest.json').read_text())


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(['/usr/bin/git', '-C', str(CS), *args], text=True).strip()


def verify():
    assert git('rev-parse', 'HEAD') == M['base'], 'source revision changed'
    assert git('branch', '--show-current') == M['branch'], 'source branch changed'
    assert git('status', '--porcelain', '--untracked-files=all') == M['expectedGitStatus'], 'source worktree drift'
    for name, digest in M['files'].items(): assert sha(CS/name) == digest, name+' changed'
    for name, digest in M['scripts'].items(): assert sha(HERE/name) == digest, name+' changed'
    approval = H/'CellProtocolDocuments/Deliverables/PDD_project-workspace_2026-10-12/evidence/g2-approval-20261013.json'
    assert sha(approval) == M['approvalSHA256'], 'G2 approval changed'
    authorization = json.loads((HERE/'AUTHORIZATION.json').read_text())
    assert authorization['jobID'] == JOB and authorization['approved'] is True
    assert authorization['manifestSHA256'] == sha(HERE/'manifest.json'), 'authorization mismatch'
    assert authorization['approvedPatchSHA256'] == M['approvedPatchSHA256']
    print('INPUT VERIFIED: frozen project baseline with one approved test correction', flush=True)


def admission():
    a = json.loads((HERE/'ADMISSION.json').read_text())
    assert a['jobID'] == JOB and a['coordinator'] == 'Deploy prosjekt køadministrasjon'
    assert a['exclusiveBuildWindow'] is True
    assert datetime.datetime.now(datetime.timezone.utc) < datetime.datetime.fromisoformat(a['expiresAt'])
    q = H/'_losen-queue'
    foreign = [p.name for p in (q/'running').glob('*.job') if p.name != JOB+'.job']
    waiting = [p.name for lane in q.glob('inbox*') for p in lane.glob('*.job') if p.name != JOB+'.job']
    assert not foreign and not waiting, ('queue occupied', foreign, waiting)


def main():
    verify()
    if len(sys.argv) != 2 or sys.argv[1] not in ('check', 'run'): raise SystemExit(64)
    if sys.argv[1] == 'check':
        print('CHECK ONLY: no Swift or activation'); return
    admission()
    env = {k:os.environ[k] for k in ('HOME','USER','LOGNAME','TMPDIR') if k in os.environ}
    env.update(PATH='/usr/bin:/bin:/usr/sbin:/sbin', LC_ALL='C', HAVEN_SWIFTPM_JOBS='2',
        HAVEN_BUILD_MIN_FREE_PERCENT='10', HAVEN_BUILD_MIN_FREE_GIB='40', HAVEN_BUILD_RESERVE_GIB='10',
        HAVEN_SWIFTPM_WAIT_SECONDS='60', HAVEN_SWIFTPM_CACHE_ROOT='/private/tmp/haven-swiftpm-bounded',
        HAVEN_SWIFTPM_RUNNER=str(HERE/'report-only-swiftpm.sh'))
    subprocess.run(['/bin/bash',str(CS/'scripts/check_build_capacity.sh'),str(CS)],env=env,check=True)
    original = (CS/'Package.resolved').read_bytes()
    (HERE/'attempt-started').mkdir()
    (HERE/'Package.resolved.before').write_bytes(original)
    resource.setrlimit(resource.RLIMIT_FSIZE,(resource.RLIM_INFINITY,resource.getrlimit(resource.RLIMIT_FSIZE)[1]))
    interruptions = []
    install_interrupt_handlers(interruptions)
    children = []
    result = dict(jobID=JOB, sourceSHA=M['base'], startedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='running')
    code = 1
    try:
        log = HERE/'baseline-tests.log'
        args = ['/bin/bash',str(CS/'scripts/run_swift_bounded.sh'),'test','--disable-automatic-resolution','--filter',M['filter']]
        with log.open('w') as output:
            status = run_owned_command(args, owner=owned_process, cwd=CS, env=env,
                stdout=output, stderr=subprocess.STDOUT, timeout=3600, started=children.append)
        result['swiftExitCode'] = status
        (HERE/'swift-exit-code.txt').write_text(str(status)+'\n')
        result['passedTests'] = validate_xctest(log.read_text(errors='replace'), M['tests'], status)
        assert (CS/'Package.resolved').read_bytes() == original, 'baseline pin bytes changed'
        prefixes = re.findall(r'running swift test with cache ([0-9a-f]+)',log.read_text())
        assert len(prefixes) == 1, 'cache identity missing'
        states = list(Path('/private/tmp/haven-swiftpm-bounded/caches').glob(prefixes[0]+'*/workspace-state.json'))
        assert len(states) == 1, 'dependency workspace state missing'
        dependencies = json.loads(states[0].read_bytes())['object']['dependencies']
        cp = [d for d in dependencies if d['packageRef']['identity'] == 'cellprotocol']
        assert len(cp) == 1 and cp[0]['state']['name'] == 'sourceControlCheckout', 'baseline used local CP'
        assert cp[0]['state']['checkoutState']['revision'] == M['cellProtocolSHA'], 'wrong CP revision'
        (HERE/'cellprotocol-dependency.json').write_text(json.dumps(cp[0],indent=2)+'\n')
        result['status'] = 'passed'; code = 0
    except BaseException as error:
        result['status'] = 'stopped'; result['reason'] = str(error)
    finally:
        with deferred_cleanup_interruptions() as cleanup_interruptions:
            after = CS/'Package.resolved'
            (HERE/'Package.resolved.after').write_bytes(after.read_bytes() if after.exists() else b'')
            if not children or children[0].anchor_reaped:
                if not after.exists() or after.read_bytes() != original: after.write_bytes(original)
                try: verify()
                except BaseException as error:
                    result['postcheckError'] = str(error); result['status'] = 'stopped'; code = 1
            else:
                result['postcheckError'] = 'group proof missing; no pin restore'; result['status'] = 'stopped'; code = 1
            if interruptions or cleanup_interruptions:
                result['interruptions'] = interruptions + cleanup_interruptions
                result['status'] = 'stopped'; code = 1
            result['finishedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            result['exitCode'] = code
            (HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
            (HERE/'exit-code.txt').write_text(str(code)+'\n')
            print('PROJECT_WORKSPACE_BASELINE_TERMINAL '+json.dumps(result), flush=True)
    raise SystemExit(code)


if __name__ == '__main__': main()
