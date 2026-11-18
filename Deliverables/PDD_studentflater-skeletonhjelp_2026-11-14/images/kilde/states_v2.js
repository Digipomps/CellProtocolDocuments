const todo = {
  activeItems: [
    { id: 't1', title: 'Les kapittel 12 om identitet', dueText: 'I morgen' },
    { id: 't2', title: 'Skriv metodeavsnitt', dueText: 'Fredag' },
    { id: 't3', title: 'Møte med Petter', dueText: 'Ingen frist' }
  ],
  completedItems: [{ id: 't0', title: 'Sett opp HAVEN-konto' }]
};
const sara = { initials: 'SA' }, ola = { initials: 'OL' };
const tabs = [{ id: 'visning', title: 'Forhåndsvisning' }, { id: 'bygget', title: 'Slik er den bygget' }];
const desc = 'Vis gjøremålene mine med frist, og la meg krysse dem av. De fullførte under.';
const details = [
  { label: 'Henter fra', value: 'Gjøremålene dine (cell:///Todo)' },
  { label: 'Viser', value: 'Aktive gjøremål med frist, og fullførte' },
  { label: 'Knapper', value: '«Ferdig» krysser av gjøremålet i raden' },
  { label: 'Sjekket', value: 'Alt kan vises, og alle knappene virker' }
];
function st(o) {
  return { configurationStudio: { state: Object.assign({
    statusLine: 'Utkast', ui: { resultTab: 'visning', resultTabs: tabs },
    coedit: { editors: [sara], conflicts: [], sharePanel: [], inviteDraft: '' },
    assist: { description: '', canDraft: [{ modelText: 'Mistral Small · EU' }], noModel: [] },
    result: [], saveBar: [] }, o) }, todo };
}
const ok = { badge: 'Klar', badgeColor: '#166534', badgeBackground: '#dcfce7', headline: 'Forslaget virker',
  explanation: 'Panelet viser gjøremålene dine og lar deg krysse dem av.', fixes: [], details };
const all = [
  { name: 'v2-tom', state: st({ assist: { description: '', canDraft: [],
      noModel: [{ text: 'Du har ikke tilgang til en språkmodell ennå. Du kan laste opp en flate du har laget selv.' }] } }) },
  { name: 'v2-utfylt', preview: true, state: st({ statusLine: 'Utkast · lagret av Ola kl. 14.05',
      coedit: { editorsText: 'Med Ola', editors: [sara, ola], conflicts: [], sharePanel: [], inviteDraft: '' },
      assist: { description: desc, canDraft: [{ modelText: 'Mistral Small · EU' }], noModel: [] },
      result: [ok], saveBar: [{ text: 'Ikke lagret ennå' }] }) },
  { name: 'v2-feil', preview: true, state: st({ statusLine: 'Utkast',
      assist: { description: 'Vis «Fullført» bare når jeg har fullførte gjøremål, med en knapp for å rydde dem.', canDraft: [{ modelText: 'Mistral Small · EU' }], noModel: [] },
      result: [{ badge: 'Må rettes', badgeColor: '#92400e', badgeBackground: '#fef3c7', headline: 'Én del av forslaget ville aldri vist seg',
        explanation: 'Seksjonen «Fullført» og knappen «Rydd» var skjult slik at de aldri kommer fram. Forslaget er ikke tatt i bruk, og forhåndsvisningen viser det forrige.',
        fixes: [{}], details: details.slice(0, 3).concat([{ label: 'Sjekket', value: '«Rydd» kan ikke nås (todo.clearCompleted)' }]) }],
      saveBar: [] }) },
  { name: 'v2-konflikt', preview: true, state: st({ statusLine: 'Utkast · Ola lagret kl. 14.07',
      coedit: { editorsText: 'Med Ola', editors: [sara, ola], conflicts: [{ title: 'Ola lagret en nyere versjon', text: 'Endringen din ble ikke lagret, fordi den bygger på en eldre versjon. Hent den nyeste, så ligger teksten din klar til å legges inn igjen.' }], sharePanel: [], inviteDraft: '' },
      assist: { description: desc, canDraft: [{ modelText: 'Mistral Small · EU' }], noModel: [] },
      result: [ok], saveBar: [] }) },
  { name: 'v2-del', preview: true, state: st({ statusLine: 'Utkast · lagret kl. 14.02',
      coedit: { editors: [sara], conflicts: [], sharePanel: [{}], inviteDraft: '' },
      assist: { description: desc, canDraft: [{ modelText: 'Mistral Small · EU' }], noModel: [] },
      result: [ok], saveBar: [] }) }
];
all.push({ name: 'v2-hjelper', skeleton: 'helper', state: { workbenchHelper: { state: { messages: [
  { who: 'Du', text: 'Lag en flate som viser oppgavene mine', bg: '#eef2ff' },
  { who: 'Hjelper', text: 'Det kan jeg ikke gjøre herfra. Denne hjelperen flytter oppgaver mellom faner. Flater lager du i Studio, der du beskriver flaten og får et forslag du kan se før du lagrer.', bg: '#ffffff' }] } } } });
module.exports = { all };
