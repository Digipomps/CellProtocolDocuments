#!/usr/bin/python3
"""Stackramme per funksjon fra arm64-prologen i objektfiler (debug-bygg).

Summerer pre-indeksert stp [sp, #-N]! og alle `sub sp, sp, #N[, lsl #12]` i de
første 16 instruksjonene. Skriver JSON {modul: {funksjon: byte}} for rammer >= 8 KiB.
"""
import json, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); out = Path(sys.argv[2])
inter = root / ".build/out/Intermediates.noindex"
dirs = [d for d in inter.glob("*/Debug/*.build") if d.name.split(".")[0].split("-")[0] in ("App", "CellBase")]
label = re.compile(r"^[0-9a-f]+ <(.*)>:$")
stp = re.compile(r"\bstp\b.*\[sp, #-0x([0-9a-f]+)\]!")
sub = re.compile(r"\bsub\s+sp, sp, #0x([0-9a-f]+)(, lsl #12)?")
result = {}
for d in sorted(dirs):
    frames = {}
    for obj in sorted(d.glob("Objects-normal/arm64/*.o")):
        asm = subprocess.run(["xcrun", "llvm-objdump", "--disassemble", "--demangle", "--no-show-raw-insn", str(obj)],
                             capture_output=True, text=True).stdout.splitlines()
        name = None; n = 0; size = 0
        for line in asm:
            m = label.match(line)
            if m:
                if name and size >= 8192:
                    frames[name] = max(size, frames.get(name, 0))
                name = m.group(1); n = 0; size = 0; continue
            if name is None or n >= 16: continue
            n += 1
            a = stp.search(line)
            if a: size += int(a.group(1), 16)
            b = sub.search(line)
            if b: size += int(b.group(1), 16) << (12 if b.group(2) else 0)
        if name and size >= 8192:
            frames[name] = max(size, frames.get(name, 0))
    result[str(d.relative_to(inter))] = frames
out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
for mod, frames in result.items():
    top = sorted(frames.items(), key=lambda kv: -kv[1])[:12]
    print(f"{mod}: {len(frames)} funksjoner >= 8 KiB")
    for k, v in top: print(f"  {v:>9}  {k[:150]}")
