#!/usr/bin/env python3
"""Generate a self-contained sketch overlay for the Hoenn reference map.

Produces one HTML file with the rendered map embedded as a data URI, so it
works offline and can be published as an artifact. Strokes are kept on a
separate canvas layered over the map image, which is what keeps drawing fast:
the map is never redrawn, only composited by the browser.

Everything exports in **world metatile coordinates**, not pixels, so a sketch
can be read straight back against map.bin. The renderer writes a header band
above the map, so image y has to lose that offset before scaling.

    python3 tools/make_sketch_tool.py --scale 8 -o hoenn_sketch.html
"""
import argparse, base64, io, json, os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = r"""<title>Open Hoenn — Sketch Overlay</title>
<style>
:root{
  color-scheme:dark;
  --bg:#14161c; --panel:#1a1d25; --panel2:#20242e; --line:#2b3040;
  --ink:#c9cedb; --dim:#7d859b; --accent:#9d7bd8; --ok:#5fb98a;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);
  font:13px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
button,select,input{font:inherit;color:inherit}
#app{display:grid;grid-template-rows:auto 1fr auto;height:100vh;height:100dvh}
header{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:8px 12px;
  background:var(--panel);border-bottom:1px solid var(--line)}
h1{margin:0;font-size:12px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);font-weight:600}
.sep{flex:1}
.badge{font-size:11px;color:var(--dim)}
.badge b{color:var(--ink);font-weight:600}
button{background:var(--panel2);border:1px solid var(--line);border-radius:3px;
  padding:5px 9px;cursor:pointer}
button:hover{border-color:var(--accent)}
button.on{background:var(--accent);border-color:var(--accent);color:#14161c;font-weight:600}
button:disabled{opacity:.4;cursor:default}
button:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
#stage{position:relative;overflow:auto;background:#0d0f14}
#sheet{position:relative;transform-origin:0 0}
#sheet img,#sheet canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
#sheet img{image-rendering:pixelated}
#ink{touch-action:none}
#ink.pan{touch-action:auto}
footer{background:var(--panel);border-top:1px solid var(--line);padding:8px 12px;
  display:flex;flex-wrap:wrap;gap:10px;align-items:center}
#pens{display:flex;flex-wrap:wrap;gap:5px}
.pen{display:flex;align-items:center;gap:5px;padding:4px 8px;border-radius:3px;
  border:1px solid var(--line);background:var(--panel2);cursor:pointer;font-size:11px}
.pen i{width:13px;height:13px;border-radius:2px;display:block;border:1px solid #0006}
.pen.on{border-color:var(--ink);background:#2c3242}
.note{color:var(--dim);font-size:11px}
@media(max-width:860px){
  h1{flex:1 0 100%}
  .sep{display:none}
  header,footer{gap:6px;padding:6px 8px}
  .pen{padding:5px 7px}
}
</style>

<div id="app">
  <header>
    <h1>Open Hoenn — Sketch Overlay</h1>
    <select id="jump"></select>
    <button id="tDraw" class="on">Draw</button>
    <button id="tPan">Pan</button>
    <button id="tLabel">Label</button>
    <button id="tErase">Erase</button>
    <span class="badge">size <b id="szLbl">6</b></span>
    <button id="szDn">&minus;</button><button id="szUp">+</button>
    <span class="sep"></span>
    <span class="badge">zoom <b id="zLbl">100%</b></span>
    <button id="zOut">&minus;</button><button id="zIn">+</button>
    <button id="undo">Undo</button>
    <button id="clr">Clear</button>
    <button id="copy" title="metatile coordinates, pasteable into chat">Copy sketch</button>
    <button id="png">Save PNG</button>
  </header>

  <div id="stage">
    <div id="sheet"><img id="bg" alt="Hoenn reference map"><canvas id="ink"></canvas></div>
  </div>

  <footer>
    <div id="pens"></div>
    <span class="note" id="hint">Pick a pen, then draw over a red gap. Label drops a
      pinned note. Copy sketch gives metatile coordinates.</span>
  </footer>
</div>

<script>
const MAP = __MAP__;          // {w,h,scale,header,gaps:[{name,x,y,w,h}]}
const PENS = [
  ['path',      '#e0c274'], ['grass',   '#57b45c'], ['tall grass', '#2e7d3a'],
  ['water',     '#4a8fd6'], ['trees',   '#1f5c33'], ['cliff',      '#9a8d80'],
  ['building',  '#e08a3c'], ['cave',    '#8a6bd0'], ['note',       '#e84a4a'],
];
const $ = id => document.getElementById(id);
let pen = 0, tool = 'draw', size = 6, zoom = 1, drawing = false;
let strokes = [], cur = null;

const img = $('bg'), ink = $('ink'), sheet = $('sheet'), stage = $('stage');
// the ink layer runs at half the map's pixel scale: plenty for impressions and
// a quarter of the memory, which matters on a phone
const DIV = 2;
const IW = MAP.w * MAP.scale, IH = MAP.h * MAP.scale + MAP.header;
ink.width = Math.round(IW / DIV); ink.height = Math.round(IH / DIV);
const cx = ink.getContext('2d');
cx.lineCap = cx.lineJoin = 'round';

function layout(){
  sheet.style.width = (IW * zoom) + 'px';
  sheet.style.height = (IH * zoom) + 'px';
  $('zLbl').textContent = Math.round(zoom * 100) + '%';
}
// canvas pixel -> world metatile, undoing the header band the renderer adds
const toMeta = (px, py) => [ (px * DIV) / MAP.scale,
                             ((py * DIV) - MAP.header) / MAP.scale ];
function at(e){
  const r = ink.getBoundingClientRect();
  return [ (e.clientX - r.left) / r.width  * ink.width,
           (e.clientY - r.top ) / r.height * ink.height ];
}

function repaint(){
  cx.clearRect(0, 0, ink.width, ink.height);
  for (const s of strokes){
    if (s.kind === 'label'){
      cx.font = `600 ${Math.max(11, 13 / DIV * 2)}px ui-monospace,monospace`;
      const w = cx.measureText(s.text).width + 10;
      cx.fillStyle = '#0d0f14ee';
      cx.fillRect(s.p[0], s.p[1] - 11, w, 17);
      cx.strokeStyle = s.color; cx.lineWidth = 1;
      cx.strokeRect(s.p[0], s.p[1] - 11, w, 17);
      cx.fillStyle = s.color;
      cx.fillText(s.text, s.p[0] + 5, s.p[1] + 2);
      continue;
    }
    cx.globalCompositeOperation = s.kind === 'erase' ? 'destination-out' : 'source-over';
    cx.strokeStyle = s.color; cx.lineWidth = s.size;
    cx.beginPath();
    s.p.forEach((q, i) => i ? cx.lineTo(q[0], q[1]) : cx.moveTo(q[0], q[1]));
    if (s.p.length === 1) cx.lineTo(s.p[0][0] + .01, s.p[0][1]);
    cx.stroke();
  }
  cx.globalCompositeOperation = 'source-over';
}

function down(e){
  if (tool === 'pan') return;
  const p = at(e);
  if (tool === 'label'){
    const t = prompt('Label:');
    if (t) { strokes.push({kind:'label', text:t, color:PENS[pen][1], p}); repaint(); }
    return;
  }
  ink.setPointerCapture(e.pointerId);
  drawing = true;
  cur = {kind: tool === 'erase' ? 'erase' : 'draw', color: PENS[pen][1],
         label: PENS[pen][0], size: size * 2 / DIV * 2, p: [p]};
  strokes.push(cur); repaint();
}
function move(e){ if (drawing){ cur.p.push(at(e)); repaint(); } }
function up(){ drawing = false; cur = null; }

function setTool(t){
  tool = t;
  ['tDraw','tPan','tLabel','tErase'].forEach(id =>
    $(id).classList.toggle('on', id.toLowerCase() === 't' + t));
  ink.classList.toggle('pan', t === 'pan');
}
function setZoom(d){
  const Z = [0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3];
  let i = Z.reduce((b, v, n) => Math.abs(v - zoom) < Math.abs(Z[b] - zoom) ? n : b, 0);
  i = Math.max(0, Math.min(Z.length - 1, i + d));
  const sx = (stage.scrollLeft + stage.clientWidth / 2) / zoom;
  const sy = (stage.scrollTop + stage.clientHeight / 2) / zoom;
  zoom = Z[i]; layout();
  stage.scrollLeft = sx * zoom - stage.clientWidth / 2;
  stage.scrollTop  = sy * zoom - stage.clientHeight / 2;
  $('zOut').disabled = i === 0; $('zIn').disabled = i === Z.length - 1;
}
function jumpTo(g){
  const zx = stage.clientWidth / (g.w * MAP.scale), zy = stage.clientHeight / (g.h * MAP.scale);
  zoom = Math.max(0.25, Math.min(2, Math.min(zx, zy) * 0.85)); layout();
  stage.scrollLeft = (g.x + g.w / 2) * MAP.scale * zoom - stage.clientWidth / 2;
  stage.scrollTop  = ((g.y + g.h / 2) * MAP.scale + MAP.header) * zoom - stage.clientHeight / 2;
}

function sketchText(){
  const out = {units: 'world metatiles', map: `${MAP.w}x${MAP.h}`, strokes: []};
  for (const s of strokes){
    if (s.kind === 'erase') continue;
    if (s.kind === 'label'){
      const m = toMeta(s.p[0], s.p[1]);
      out.strokes.push({pen: 'label', text: s.text, at: m.map(v => +v.toFixed(1))});
    } else {
      const pts = s.p.filter((_, i) => i % 3 === 0 || i === s.p.length - 1)
                     .map(q => toMeta(q[0], q[1]).map(v => +v.toFixed(1)));
      out.strokes.push({pen: s.label, points: pts});
    }
  }
  return JSON.stringify(out);
}
function copyText(t){
  const done = ok => { const b = $('copy');
    b.textContent = ok ? 'Copied' : 'Copy failed';
    setTimeout(() => b.textContent = 'Copy sketch', 1400); };
  if (navigator.clipboard && window.isSecureContext)
    navigator.clipboard.writeText(t).then(() => done(true), () => fallback(t, done));
  else fallback(t, done);
}
function fallback(t, done){
  const a = document.createElement('textarea');
  a.value = t; a.style.cssText = 'position:fixed;top:8px;left:8px;width:90vw;height:40vh;z-index:9';
  document.body.appendChild(a); a.select();
  let ok = false; try { ok = document.execCommand('copy'); } catch(_){}
  if (ok) a.remove(); else setTimeout(() => a.remove(), 15000);
  done(ok);
}

function boot(){
  if (!document.querySelector('meta[name="viewport"]')){
    const m = document.createElement('meta');
    m.name = 'viewport'; m.content = 'width=device-width,initial-scale=1';
    document.head.appendChild(m);
  }
  img.src = 'data:image/png;base64,' + MAPDATA;
  const p = $('pens');
  PENS.forEach(([name, col], i) => {
    const b = document.createElement('button');
    b.className = 'pen' + (i === 0 ? ' on' : '');
    b.innerHTML = `<i style="background:${col}"></i>${name}`;
    b.onclick = () => { pen = i;
      [...p.children].forEach((k, n) => k.classList.toggle('on', n === i)); };
    p.appendChild(b);
  });
  const j = $('jump');
  j.appendChild(new Option('jump to…', ''));
  MAP.gaps.forEach((g, i) => j.appendChild(new Option(g.name, i)));
  j.onchange = () => { if (j.value !== '') jumpTo(MAP.gaps[+j.value]); };

  $('tDraw').onclick = () => setTool('draw');
  $('tPan').onclick = () => setTool('pan');
  $('tLabel').onclick = () => setTool('label');
  $('tErase').onclick = () => setTool('erase');
  $('szUp').onclick = () => { size = Math.min(40, size + 2); $('szLbl').textContent = size; };
  $('szDn').onclick = () => { size = Math.max(2, size - 2); $('szLbl').textContent = size; };
  $('zIn').onclick = () => setZoom(+1);
  $('zOut').onclick = () => setZoom(-1);
  $('undo').onclick = () => { strokes.pop(); repaint(); };
  $('clr').onclick = () => { if (confirm('Clear the whole sketch?')){ strokes = []; repaint(); } };
  $('copy').onclick = () => copyText(sketchText());
  $('png').onclick = () => {
    const c = document.createElement('canvas');
    c.width = IW; c.height = IH;
    const g = c.getContext('2d');
    g.drawImage(img, 0, 0, IW, IH);
    g.drawImage(ink, 0, 0, IW, IH);
    const a = document.createElement('a');
    a.href = c.toDataURL('image/png'); a.download = 'hoenn_sketch.png'; a.click();
  };
  ink.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button === 0) down(e);
  });
  ink.addEventListener('pointermove', move);
  window.addEventListener('pointerup', up);
  window.addEventListener('pointercancel', up);
  layout();
  img.onload = () => { if (MAP.gaps.length) jumpTo(MAP.gaps[0]); };
}
boot();
</script>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scale', type=int, default=8)
    ap.add_argument('-o', '--out', default='hoenn_sketch.html')
    a = ap.parse_args()

    png = os.path.join(HERE, '..', f'_sketch_bg_{a.scale}.png')
    subprocess.run([sys.executable, os.path.join(HERE, 'render_hoenn.py'),
                    '--scale', str(a.scale), '-o', png], check=True)
    raw = open(png, 'rb').read()
    im = Image.open(png)
    print(f'background {im.size}, {len(raw)/1e6:.1f} MB', file=sys.stderr)

    # gap boxes come from the same solver the renderer uses
    sys.path.insert(0, HERE)
    import render_hoenn as R
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    W = max(x + lay[maps[k]['layout']]['width'] for k, (x, y) in pos.items()) - minx
    H = max(y + lay[maps[k]['layout']]['height'] for k, (x, y) in pos.items()) - miny
    occ = {}
    for k, (x, y) in pos.items():
        L = lay[maps[k]['layout']]
        for yy in range(y, y + L['height']):
            for xx in range(x, x + L['width']):
                occ[(xx - minx, yy - miny)] = k
    regs = [r for r in R.empty_regions(occ, W, H) if r[0] >= 2000]
    inland = [r for r in regs if len({k.replace('MAP_', '') for k in r[2]} & R.WATER) < 2]
    gaps = []
    for i, (n, comp, bd) in enumerate(inland[:5]):
        xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
        gaps.append({'name': f'{R.GAPS[i][0]} — {R.GAPS[i][1]}', 'x': min(xs), 'y': min(ys),
                     'w': max(xs) - min(xs) + 1, 'h': max(ys) - min(ys) + 1})
    meta = {'w': W, 'h': H, 'scale': a.scale, 'header': a.scale * 11, 'gaps': gaps}

    html = TEMPLATE.replace('__MAP__', json.dumps(meta))
    html = html.replace('boot();', 'boot();', 1)
    b64 = base64.b64encode(raw).decode()
    html = html.replace('<script>', '<script>\nconst MAPDATA = "' + b64 + '";', 1)
    open(a.out, 'w').write(html)
    os.remove(png)
    print(f'wrote {a.out} ({os.path.getsize(a.out)/1e6:.1f} MB)', file=sys.stderr)

if __name__ == '__main__':
    sys.exit(main())
