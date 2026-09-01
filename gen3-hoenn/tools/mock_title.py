import sys, struct
from PIL import Image, ImageDraw, ImageFilter
SD = sys.argv[1]; G = 'graphics/title_screen'

def flat(name):
    """a PNG whose .bin is an identity map - the picture is the file."""
    im = Image.open(f'{G}/{name}').convert('RGBA'); p = im.load()
    bg = p[0, 0]
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y] == bg: p[x, y] = (0, 0, 0, 0)
    return im

def mapped(binf, pngf):
    """a real 32-wide tilemap over the PNG's own tiles and palette."""
    tiles = Image.open(f'{G}/{pngf}').convert('RGBA')
    tp = tiles.load(); bg = tp[0, 0]
    for y in range(tiles.height):
        for x in range(tiles.width):
            if tp[x, y] == bg: tp[x, y] = (0, 0, 0, 0)
    tw = tiles.width // 8
    d = open(f'{G}/{binf}', 'rb').read()
    tm = struct.unpack(f'<{len(d)//2}H', d)
    H = len(tm) // 32
    out = Image.new('RGBA', (32*8, H*8), (0, 0, 0, 0))
    for i, v in enumerate(tm):
        t = v & 0x3FF
        if t >= tw * (tiles.height // 8): continue
        c = tiles.crop(((t % tw)*8, (t//tw)*8, (t % tw)*8+8, (t//tw)*8+8))
        if (v >> 10) & 1: c = c.transpose(Image.FLIP_LEFT_RIGHT)
        if (v >> 11) & 1: c = c.transpose(Image.FLIP_TOP_BOTTOM)
        out.paste(c, ((i % 32)*8, (i//32)*8), c)
    return out

STROKE, OUTLINE = 5, (24, 16, 24)
WIDTHS = {'O': 21, 'H': 20, 'E': 17, 'N': 20, 'P': 18}

def letter(ch, w, h):
    m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    s = STROKE; r = s // 2
    bar = lambda a, b, c2, e: d.line([(a, b), (c2, e)], fill=255, width=s, joint='curve')
    L, R, T, B, MY = r, w-r-1, r, h-r-1, h//2
    if ch == 'O':   d.ellipse([r-2, 0, w-r+1, h-1], outline=255, width=s)
    elif ch == 'H': bar(L, T, L, B); bar(R, T, R, B); bar(L, MY, R, MY)
    elif ch == 'E': bar(L, T, L, B); bar(L, T, R, T); bar(L, MY, R-2, MY); bar(L, B, R, B)
    elif ch == 'N': bar(L, T, L, B); bar(R, T, R, B); bar(L, T-1, R, B+1)
    elif ch == 'P': bar(L, T, L, B); bar(L, T, R, T); bar(R, T, R, MY); bar(L, MY, R, MY)
    return m

def word(text, lh, arch=4):
    tot = sum(WIDTHS[c] for c in text)
    pad = 12
    canvas = Image.new('RGBA', (tot + pad*2, lh + pad*2 + arch), (0, 0, 0, 0))
    x, n = pad, len(text)
    for i, ch in enumerate(text):
        w = WIDTHS[ch]
        m = letter(ch, w, lh)
        t = (i - (n-1)/2) / max(1, (n-1)/2)
        g = Image.new('RGBA', m.size); gd = ImageDraw.Draw(g)
        for yy in range(lh):
            k = yy / max(1, lh-1)
            c = int(255 - 120*k*k*k)
            gd.line([(0, yy), (w, yy)], fill=(c, c, c, 255))
        face = Image.new('RGBA', m.size, (0, 0, 0, 0))
        face.paste(g, (0, 0), m)
        # arch by vertical offset only. Rotating each letter expands its box,
        # which moved every origin and ran the letters into each other.
        canvas.alpha_composite(face, (x, pad + int(arch * t * t)))
        x += w + 1
    a = canvas.split()[3].point(lambda v: 255 if v > 90 else 0)
    ring = Image.new('RGBA', canvas.size, OUTLINE + (255,))
    out = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    out.paste(ring, (0, 0), a.filter(ImageFilter.MaxFilter(5)))
    out.paste(canvas, (0, 0), a)
    return out.crop(out.getbbox())

logo, ray, clouds = flat('pokemon_logo.png'), mapped('rayquaza.bin', 'rayquaza.png'), mapped('clouds.bin', 'clouds.png')
press = flat('press_start.png')
orig = flat('emerald_version.png'); orig = orig.crop(orig.getbbox())

w1, w2 = word('OPEN', 18, arch=3), word('HOENN', 23, arch=4)
new = Image.new('RGBA', (max(w1.width, w2.width), w1.height + w2.height - 8), (0, 0, 0, 0))
new.alpha_composite(w1, ((new.width - w1.width)//2, 0))
new.alpha_composite(w2, ((new.width - w2.width)//2, w1.height - 7))

def scene(wm):
    im = Image.new('RGBA', (240, 160), (12, 40, 56, 255))
    im.alpha_composite(clouds.crop((0, 0, 240, 160)), (0, 0))
    im.alpha_composite(ray.crop((0, 0, 240, 160)), (0, 0))
    im.alpha_composite(logo.crop((0, 0, 240, min(64, logo.height))), (0, 10))
    im.alpha_composite(wm, (238 - wm.width, 76))
    im.alpha_composite(press, (40, 126))
    return im.convert('RGB')

S = 3
out = Image.new('RGB', (240*S*2 + 24, 160*S + 34), (18, 18, 18))
d = ImageDraw.Draw(out)
for i, (wm, cap) in enumerate(((orig, 'BEFORE  (vanilla)'), (new, 'AFTER  (only the wordmark changes)'))):
    out.paste(scene(wm).resize((240*S, 160*S), Image.NEAREST), (8 + i*(240*S+8), 8))
    d.text((12 + i*(240*S+8), 160*S + 14), cap, fill=(225, 225, 225))
out.save(f'{SD}/title_mock.png')
new.resize((new.width*5, new.height*5), Image.NEAREST).save(f'{SD}/wordmark.png')
print('wordmark', new.size)
