#!/usr/bin/env python3
"""Mockups for PDD_butler-onboarding-og-formaalsforstaaelse (G1-GUI).

Base: the real Butler workbench screenshot (local test host, same code as prod 77a922bc,
evidence/web-regresjon/plassering/sonde-etter.png). Only the centre panel's content area is
redrawn; everything else is the real rendering.
"""
import base64, pathlib

B64 = base64.b64encode(pathlib.Path("base.png").read_bytes()).decode()

CSS = """
*{box-sizing:border-box}
body{margin:0;width:1280px;height:900px;position:relative;font-family:"Liberation Sans",Arial,sans-serif;color:#0f172a}
.bg{position:absolute;inset:0;background:url(data:image/png;base64,%s) no-repeat 0 0/1280px 900px}
.area{position:absolute;left:336px;top:366px;width:528px;height:504px;background:#fff;border-radius:0 0 10px 10px}
.log{position:absolute;left:30px;right:30px;top:14px;display:flex;flex-direction:column;gap:10px}
.sys{font-size:13px;color:#475569;line-height:1.45}
.card{border:1px solid #d5e0eb;border-radius:10px;padding:12px 14px;font-size:15px;line-height:1.45;background:#fff}
.card h4{margin:0 0 6px;font-size:13px;font-weight:700;color:#0f8a61;letter-spacing:.2px}
.card.q{border-left:3px solid #0f8a61}
.card.err{border-left:3px solid #b8860b;background:#fffbeb}
.card.err h4{color:#92400e}
.me{align-self:flex-end;background:#0f4c81;color:#fff;border-radius:12px 12px 2px 12px;padding:8px 12px;font-size:14px;max-width:70%%}
.me.redacted{background:#e2e8f0;color:#334155;font-style:italic}
.btns{display:flex;gap:8px;margin-top:10px}
.btn{border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;font-size:13px;font-weight:700;background:#fff;color:#0f172a}
.btn.pri{background:#0f4c81;border-color:#0f4c81;color:#fff}
.hr{position:absolute;left:14px;right:14px;height:1px;background:#d5e0eb}
.mode{white-space:nowrap;position:absolute;left:14px;right:14px;height:40px;background:#ecfdf7;border:1px solid #9fe6cf;border-left:4px solid #0f8a61;border-radius:8px;display:flex;align-items:center;padding:0 12px;font-size:13px;gap:10px}
.mode b{color:#065f46}
.dots{display:flex;gap:5px;margin-left:4px}
.dot{width:9px;height:9px;border-radius:50%%;background:#bfe9da;border:1px solid #0f8a61}
.dot.on{background:#0f8a61}
.dot.now{background:#fff;box-shadow:0 0 0 2px #0f8a61}
.mode .end{margin-left:auto;color:#0f4c81;font-weight:700;text-decoration:underline}
.composer{position:absolute;left:30px;width:400px;height:42px;border:1px solid #d5e0eb;border-radius:6px;padding:0 12px;display:flex;align-items:center;font-size:15px;color:#64748b;background:#fff}
.composer.onb{border:2px solid #0f8a61;background:#f6fffb;color:#3f6b5c}
.composer.secret{border:2px solid #0f8a61;background:#f6fffb;color:#0f172a;letter-spacing:3px;font-size:18px}
.send{white-space:nowrap;position:absolute;left:439px;height:34px;border-radius:5px;background:#0f4c81;color:#fff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;padding:0 12px}
.foot{white-space:nowrap;position:absolute;left:30px;right:30px;font-size:12.5px;color:#475569;display:flex;align-items:center;gap:8px}
.chip{border:1px solid #cbd5e1;border-radius:999px;padding:2px 8px;font-size:12px;color:#334155;background:#fff}
.chip.onb{border-color:#0f8a61;color:#065f46;background:#ecfdf7}
.foot .r{margin-left:auto;font-weight:700;color:#334155}
.lock{display:inline-block;width:14px;height:14px;margin-right:8px;vertical-align:-2px}
.tag{position:absolute;right:10px;top:8px;font-size:11px;color:#94a3b8}
""" % B64

LOCK = '<svg class="lock" viewBox="0 0 16 16"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="#0f8a61"/><path d="M5 7V5a3 3 0 0 1 6 0v2" stroke="#0f8a61" stroke-width="1.6" fill="none"/></svg>'


def page(inner):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='bg'></div><div class='area'>{inner}</div></body></html>"


steg = page("""
<div class="log">
  <div class="sys">Du trykket «Koble til modell». Butler stiller tre spørsmål. Ingenting lagres før du bekrefter det siste steget.</div>
  <div class="card q"><h4>STEG 1 AV 3 · LEVERANDØR OG MODELL</h4>
    Hvilken leverandør og modell vil du koble til? For eksempel 4o-mini fra OpenAI, Claude fra Anthropic, eller en lokal modell via Ollama eller llama.cpp.</div>
</div>
<div class="hr" style="top:352px"></div>
<div class="mode" style="top:364px"><b>Onboarding pågår</b> · Koble til modell · steg 1 av 3
  <span class="dots"><span class="dot now"></span><span class="dot"></span><span class="dot"></span></span>
  <span class="end">Avbryt onboarding</span></div>
<div class="composer onb" style="top:414px">Svar på steg 1: leverandør og modell …</div>
<div class="send" style="top:418px;width:62px">Svar</div>
<div class="foot" style="top:468px">Svaret går til onboardingen, ikke til chatten. <span class="chip onb">svarer på: steg 1 av 3</span><span class="r">Hopp over</span></div>
""")

noekkel = page("""
<div class="log">
  <div class="card q" style="padding:8px 14px"><h4 style="margin:0">STEG 1 AV 3 · LEVERANDØR OG MODELL</h4></div>
  <div class="me">Claude fra Anthropic</div>
  <div class="card q" style="padding:8px 14px"><h4 style="margin:0">STEG 2 AV 3 · ALIAS FOR NØKKELEN</h4></div>
  <div class="me">anthropic</div>
  <div class="card q"><h4>STEG 3 AV 3 · API-NØKKEL (HEMMELIG)</h4>
    Lim inn API-nøkkelen fra leverandøren. Den vises ikke, legges ikke i chatloggen, og lagres bare i din egen nøkkellagring når du bekrefter.</div>
</div>
<div class="hr" style="top:352px"></div>
<div class="mode" style="top:364px"><b>Onboarding pågår</b> · steg 3 av 3 · <b>hemmelig felt</b>
  <span class="dots"><span class="dot on"></span><span class="dot on"></span><span class="dot now"></span></span>
  <span class="end">Avbryt onboarding</span></div>
<div class="composer secret" style="top:414px;width:350px">""" + LOCK + """••••••••••••••••••••••</div>
<div class="send" style="top:418px;left:389px;width:116px;font-size:13px">Bekreft og lagre</div>
<div class="foot" style="top:468px">Tegnene skjules. I chatten står bare «nøkkel lagret».<span class="r">Hopp over</span></div>
""")

feil = page("""
<div class="log">
  <div class="card" style="padding:10px 14px;font-size:14px;color:#334155">Ingen modell er koblet til. Butler svarer nå med lokale regler, ikke en språkmodell.</div>
  <div class="card err"><h4>ONBOARDINGEN KUNNE IKKE STARTE</h4>
    <b>Årsak:</b> onboarding-cellen er ikke registrert i denne kjøringen av HAVEN.<br>
    Det er en feil hos oss, ikke noe du har gjort. Chatten virker som før.
    <div style="font-size:12.5px;color:#78716c;margin-top:6px">Kode: guided_onboarding_not_registered · de to andre mulige årsakene har egne koder: tilgang nektet, og steget avvist</div>
    <div class="btns"><span class="btn">Prøv igjen</span><span class="btn">Meld feil</span></div></div>
</div>
<div class="hr" style="top:372px"></div>
<div class="composer" style="top:404px">Skriv til Butler …</div>
<div class="send" style="top:408px;width:60px">Send</div>
<div class="foot" style="top:466px">Alt widgetene kan gjøre, kan du be om her. <span class="chip">skriver til: Butler</span><span class="r">Rydd utkast</span></div>
""")

for name, html in [("butler-onboarding-steg-v1", steg), ("butler-onboarding-noekkel-v1", noekkel), ("butler-onboarding-feil-v1", feil)]:
    pathlib.Path(f"{name}.html").write_text(html, encoding="utf-8")
print("ok")
