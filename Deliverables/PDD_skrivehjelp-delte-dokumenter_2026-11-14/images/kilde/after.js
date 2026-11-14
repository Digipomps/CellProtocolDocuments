const { shot } = require('./render.js');
const out = process.argv[2];
// Builds the proposed Skrivehjelp panel inside the real help section.
function build(state) {
  const h3 = [...document.querySelectorAll('h3')].find(h => h.textContent === 'Skrivehjelp');
  const root = h3.parentElement; root.innerHTML = '';
  const css = document.createElement('style'); css.textContent = `
    .assist-head{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:baseline;margin-bottom:10px}
    .assist-head h3{margin:0}
    .assist-route{font-size:13px;color:#50675b}
    .assist-note{font-size:13px;color:#50675b;margin:0 0 12px;max-width:760px}
    .assist-quote{border-left:3px solid #d8b331;background:#fdf8e6;padding:8px 12px;margin:8px 0;font:15px/1.5 Georgia,serif;white-space:pre-wrap}
    .assist-quote small{display:block;font:12px system-ui;color:#6b6440;margin-bottom:4px}
    .assist-modes{display:flex;gap:16px;margin:10px 0;flex-wrap:wrap;font-size:14px}
    .assist-entry{margin-top:14px;padding:14px;border:1px solid #dee5df;border-radius:8px;background:#fbfcf9}
    .assist-entry .who{font-size:13px;color:#50675b}
    .assist-proposal{background:#eef6f0;border:1px solid #cfe3d5;border-radius:6px;padding:10px 12px;font:15px/1.55 Georgia,serif;margin:8px 0;white-space:pre-wrap}
    .assist-actions{display:flex;gap:8px;flex-wrap:wrap}
    .assist-done{font-size:13px;color:#28774b}
    .assist-warn{background:#fff4e5;border:1px solid #f0cf9a;border-radius:8px;padding:12px 14px;margin:10px 0;font-size:14px}
    .assist-off{background:#f3f6f3;border:1px dashed #b9c9bd;border-radius:8px;padding:14px;font-size:14px}
    .haven-document .assist-actions button.primary{background:#28774b;color:#fff;border-color:#28774b}`;
  document.head.appendChild(css);
  const html = [];
  const head = (route) => `<div class="assist-head"><h3>Skrivehjelp</h3><span class="assist-route">${route}</span></div>`;
  const quote = `<div class="assist-quote"><small>Markert tekst som sendes med</small>Vi undersøker hvordan EntityAnchor og domeneavgrensede identiteter kan gi en slik unik representasjon, og hva som skjer når en identitet trekkes tilbake eller kompromitteres, og hvilke garantier som da fortsatt holder for de andre domenene som personen deltar i.</div>`;
  const form = (btn, off) => `<div class="assist-modes" role="radiogroup" aria-label="Hva slags hjelp"><label><input type="radio" name="m" checked> Foreslå ny tekst</label><label><input type="radio" name="m"> Forklar eller gi tilbakemelding</label><label><input type="radio" name="m"> Bare bruksråd (uten modell)</label></div>
    <textarea aria-label="Spør skrivehjelpen" placeholder="Hva vil du ha hjelp til?">${state==='on'?'Del setningen i to og gjør den lettere å lese':''}</textarea>
    <div class="assist-actions" style="margin-top:8px"><button class="primary" ${off?'disabled title="Velg en modell først"':''}>${btn}</button></div>`;
  const entryApplied = `<div class="assist-entry"><div class="who"><b>Petter</b> spurte · Mistral Small (EU) · betalt av Petter</div><p style="margin:6px 0">Forklar forskjellen på EntityAnchor og identitet i ett avsnitt.</p><div class="assist-proposal" style="font:14px/1.5 system-ui;background:#f6f8f6">En identitet er én nøkkel i ett domene. En EntityAnchor binder flere slike identiteter til samme person uten å gjøre dem like.</div><span class="assist-done">Forklaring, ingen endring i teksten</span></div>`;
  const entryProposal = `<div class="assist-entry"><div class="who"><b>Sara</b> spurte · Mistral Small (EU) · betalt av Sara · revisjon 13</div><p style="margin:6px 0">Del setningen i to og gjør den lettere å lese</p>
    <div class="assist-proposal">Vi undersøker hvordan EntityAnchor og domeneavgrensede identiteter kan gi en slik unik representasjon. Vi ser også på hva som skjer når en identitet trekkes tilbake eller blir kompromittert, og hvilke garantier som da fortsatt gjelder i de andre domenene personen deltar i.</div>
    <div class="assist-actions"><button class="primary">Bruk forslaget</button><button>Kopier</button><button>Forkast</button></div></div>`;
  if (state === 'on') {
    html.push(head('Språkmodell: Mistral Small (EU) · din egen tilkobling'));
    html.push(`<p class="assist-note">Spørsmålet og den markerte teksten sendes til modellen du har valgt. Alle i dokumentet ser spørsmålet og svaret. Et forslag endrer ingenting før noen velger Bruk forslaget.</p>`);
    html.push(quote, form('Spør modellen'), entryProposal, entryApplied);
  } else if (state === 'off') {
    html.push(head('Modellhjelp er av for dette dokumentet'));
    html.push(`<div class="assist-off"><b>Bare bruksråd uten språkmodell.</b> Hvis du slår på modellhjelp, kan deltakerne sende spørsmål og markert tekst fra dette dokumentet til sin egen valgte modell. Alle deltakerne får beskjed i dokumentet, og hver forespørsel vises med hvem som spurte og hvilken modell som svarte.<div class="assist-actions" style="margin-top:10px"><button class="primary">Slå på modellhjelp for dokumentet</button></div></div>`);
    html.push(`<div class="assist-entry"><div class="who"><b>Kari</b> spurte · bruksråd uten modell</div><p style="margin:6px 0">Hvordan eksporterer jeg til Word?</p><div class="assist-proposal" style="font:14px/1.5 system-ui;background:#f6f8f6">Bruk Last ned og velg Markdown, PDF eller Word.</div></div>`);
  } else if (state === 'error') {
    html.push(head('Du har ikke valgt en språkmodell'));
    html.push(`<div class="assist-warn"><b>Ingen forespørsel er sendt.</b> Modellhjelp er slått på i dokumentet, men du har ikke valgt en modell i HAVEN ennå. Velg en modell i AI Agent Workspace, så kan du spørre her. Bruksråd uten modell virker fortsatt.<div class="assist-actions" style="margin-top:10px"><button>Velg modell</button></div></div>`);
    html.push(quote, form('Spør modellen', true));
    html.push(`<div class="assist-entry"><div class="who"><b>Sara</b> spurte · Mistral Small (EU) · betalt av Sara · revisjon 9</div><p style="margin:6px 0">Gjør metodeavsnittet mer presist</p><div class="assist-proposal" style="opacity:.6">Vi bygger en prototyp med to CellScaffold-instanser og måler hvilke attributter som kan kobles mellom domener.</div><div class="assist-warn" style="margin:6px 0 0">Teksten forslaget gjelder er endret siden revisjon 9. Forslaget kan ikke brukes automatisk. Kopier det, eller be om et nytt.</div><div class="assist-actions" style="margin-top:8px"><button>Kopier</button><button>Be om nytt forslag</button></div></div>`);
  }
  root.innerHTML = html.join('');
  // mark the selected passage in the editor
  if (state !== 'off') {
    const p = [...document.querySelectorAll('.ql-editor p')][0];
    if (p) p.innerHTML = p.innerHTML.replace(/(Vi undersøker[^]*deltar i\.)/, '<span style="background:#cfe0ff">$1</span>');
  }
  const status = [...document.querySelectorAll('.document-status')].find(s => s.textContent.startsWith('Skrivehjelp'));
  if (status) status.textContent = state === 'off' ? 'Skrivehjelp · bruksråd deles i dokumentet' : 'Skrivehjelp · spørsmål, svar og forslag deles i dokumentet';
}
(async () => {
  for (const [w, h, suffix] of [[1280, 900, 'laptop'], [390, 844, 'iphone']]) {
    for (const st of ['on', 'off', 'error']) {
      const name = { on: 'forslag', off: 'av', error: 'feil' }[st];
      await shot(w, h, `skrivehjelp-${name}-${suffix}-v1.png`, new Function(`(${build.toString()})(${JSON.stringify(st)})`));
    }
  }
})();
