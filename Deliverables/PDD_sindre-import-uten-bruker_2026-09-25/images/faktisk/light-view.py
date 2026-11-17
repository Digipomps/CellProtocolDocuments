from pathlib import Path
root = Path('/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_sindre-import-uten-bruker_2026-09-25/images/faktisk')
for name in ('verk-forvaltet', 'verk-bekreftet'):
    text = (root / (name + '.html')).read_text()
    marker = '@media (prefers-color-scheme:dark)'
    assert text.count(marker) == 1
    # Capture-only equivalent of emulating a light color-scheme. Preserve the
    # original HTTP response; change no content, assets, geometry or base CSS.
    light = text.replace(marker, '@media not all')
    (root / (name + '-lys-visning.html')).write_text(light)
