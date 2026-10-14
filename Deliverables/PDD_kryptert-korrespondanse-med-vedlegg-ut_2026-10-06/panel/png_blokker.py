# -*- coding: utf-8 -*-
import sys, struct, hashlib, zlib
for f in sys.argv[1:]:
    b = open(f, 'rb').read()
    assert b[:8] == b'\x89PNG\r\n\x1a\n', f
    i = 8; typer = []; idat = b''; ekstra = {}
    while i < len(b):
        n, t = struct.unpack('>I4s', b[i:i+8]); d = b[i+8:i+8+n]; i += 12 + n
        t = t.decode('latin1'); typer.append('%s:%d' % (t, n))
        if t == 'IDAT': idat += d
        elif t not in ('IHDR', 'IEND'): ekstra[t] = d
    kort = []; forrige = None; ant = 0; sum_n = 0
    for x in typer:
        t, n = x.split(':'); n = int(n)
        if t == forrige: ant += 1; sum_n += n
        else:
            if forrige: kort.append('%s x%d (%d)' % (forrige, ant, sum_n))
            forrige, ant, sum_n = t, 1, n
    kort.append('%s x%d (%d)' % (forrige, ant, sum_n))
    raa = zlib.decompress(idat)
    print(f.split('/')[-1], 'fil', len(b), 'md5', hashlib.md5(b).hexdigest())
    print('   blokker:', ', '.join(kort))
    print('   IDAT sammensatt md5', hashlib.md5(idat).hexdigest(), 'pakket ut', len(raa), 'md5', hashlib.md5(raa).hexdigest())
    for t, d in ekstra.items():
        merker = [m for m in (b'jumb', b'jumd', b'c2pa', b'c2ma', b'cbor', b'urn:', b'claim', b'Anthropic', b'anthropic', b'Claude', b'claude', b'adobe', b'contentauth') if m in d]
        print('   ekstra', t, len(d), 'byte; kjente merker i innholdet:', ', '.join(m.decode() for m in merker) or 'ingen')
