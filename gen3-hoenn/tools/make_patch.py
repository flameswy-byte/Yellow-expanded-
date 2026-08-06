#!/usr/bin/env python3
"""Emit an IPS patch from a vanilla build to the modified one.

A built pokeemerald.gba is a complete copy of Pokémon Emerald with the hack
applied - Nintendo's game, not ours - so what gets handed around is the
difference, and the player applies it to a ROM they already own. That is what
every romhack ships and it is the only artifact this project produces.

Both ROMs are 16 MB, which is exactly the largest file IPS can address, so no
truncation or expansion record is ever needed.

    python3 tools/make_patch.py vanilla.gba pokeemerald.gba -o openhoenn.ips
"""
import argparse, os, sys

EOF_MARK = 0x454F46          # "EOF" - an offset that can never start a record
MAX_CHUNK = 0xFFFF
MIN_RLE = 10                 # below this, a literal record is smaller

def records(a, b):
    """runs of differing bytes, as (offset, data) pairs."""
    n = len(a)
    i = 0
    while i < n:
        if a[i] == b[i]:
            i += 1
            continue
        j = i
        same = 0
        # keep a run going across short identical stretches: two records cost
        # 10 bytes of header, so bridging up to that much is cheaper
        while j < n and same < 10:
            same = same + 1 if a[j] == b[j] else 0
            j += 1
        end = j - same
        yield i, b[i:end]
        i = end

def emit(off, data, out, mo):
    # an offset of 0x454F46 reads as the end of the patch, so a record can
    # never start there. Back it up one byte and carry the unchanged byte
    # before it along, which is always safe.
    if off == EOF_MARK and off > 0:
        off -= 1
        data = bytes([mo[off]]) + data
    while data:
        chunk, data = data[:MAX_CHUNK], data[MAX_CHUNK:]
        run = len(chunk) if len(set(chunk)) == 1 else 0
        if run >= MIN_RLE:
            out += off.to_bytes(3, 'big') + b'\x00\x00' + run.to_bytes(2, 'big') \
                 + bytes([chunk[0]])
        else:
            out += off.to_bytes(3, 'big') + len(chunk).to_bytes(2, 'big') + chunk
        off += len(chunk)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('vanilla')
    ap.add_argument('modified')
    ap.add_argument('-o', '--out', default='openhoenn.ips')
    a = ap.parse_args()
    va = open(a.vanilla, 'rb').read()
    mo = open(a.modified, 'rb').read()
    if len(va) != len(mo):
        raise SystemExit(f'size mismatch: {len(va)} vs {len(mo)}')
    if len(va) > 0x1000000:
        raise SystemExit('over 16 MB, which IPS cannot address')

    out = bytearray(b'PATCH')
    n = diff = 0
    for off, data in records(va, mo):
        emit(off, data, out, mo)
        n += 1
        diff += len(data)
    out += b'EOF'
    open(a.out, 'wb').write(out)
    print(f'{n} records, {diff:,} bytes changed of {len(va):,} '
          f'({100.0*diff/len(va):.2f}%)')
    print(f'wrote {a.out} ({os.path.getsize(a.out)/1e6:.2f} MB)')

if __name__ == '__main__':
    sys.exit(main())
