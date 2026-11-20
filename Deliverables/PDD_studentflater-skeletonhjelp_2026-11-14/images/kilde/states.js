const todo = {
  activeItems: [
    { id: 't1', title: 'Les kapittel 12 om identitet', dueText: 'Frist i morgen' },
    { id: 't2', title: 'Skriv metodeavsnitt', dueText: 'Frist fredag' },
    { id: 't3', title: 'Møte med Petter', dueText: 'Ingen frist' }
  ],
  completedItems: [{ id: 't0', title: 'Sett opp HAVEN-konto' }]
};
const editors = [
  { name: 'Sara (eier)', roleText: 'kan redigere', lastChangeText: 'endret 14:02' },
  { name: 'Ola', roleText: 'kan redigere', lastChangeText: 'endret 14:05' }
];
const base = (assist, extra) => ({ configurationStudio: { state: Object.assign({
  assist, reachability: { summary: '', findings: [] }, previewCaption: 'Ingen utkast ennå.',
  coedit: { editors: [editors[0]], revisionText: '', conflicts: [], inviteDraft: '' } }, extra) }, todo });

const all = [
  { name: 'studio-utkast-tom', state: base({ description: '', modelText: 'Ingen modell er tilgjengelig for kontoen din ennå. Du kan fortsatt laste opp et utkast du har laget selv; se guiden «Lag din egen flate».', messages: [] }) },
  { name: 'studio-utkast-utfylt', preview: true, state: base(
      { description: 'Et panel som viser gjøremålene mine med frist, og lar meg krysse dem av. Vis de fullførte under.',
        modelText: 'Modell: Mistral Small (EU), via tilgangen din.',
        messages: [{ title: 'Utkast laget', text: 'Bruker cell:///Todo. Leser todo.activeItems og todo.completedItems. Knappen «Ferdig» kjører todo.toggleTodo med radens id.' }] },
      { reachability: { summary: 'Sjekket: alle elementer kan vises. 1 handling kan nås: todo.toggleTodo.', findings: [] },
        previewCaption: 'Forhåndsvisning av utkastet med dine egne data.',
        coedit: { editors, revisionText: 'Revisjon 4 · sist lagret av Ola 14:05', conflicts: [], inviteDraft: '' } }) },
  { name: 'studio-utkast-feil', preview: true, state: base(
      { description: 'Vis bare «Fullført» når jeg har fullførte gjøremål, med en knapp for å rydde dem.',
        modelText: 'Modell: Mistral Small (EU), via tilgangen din.',
        messages: [
          { title: 'Utkastet har en flate som skjuler seg selv', text: 'Modellen gjemte seksjonen «Fullført» bak en betingelse på toppnivå. Den blir aldri synlig, og knappen der kan ikke nås. Studio har ikke tatt i bruk utkastet.' },
          { title: 'Forslag', text: 'Legg de fullførte i en liste. En tom liste viser ingenting, så seksjonen kommer og går av seg selv.' }] },
      { reachability: { summary: '1 funn. Handlinger flaten trenger, men som ikke kan nås: todo.clearCompleted.',
          findings: [{ title: 'Section «Fullført» kan aldri vises', detail: 'visibility på toppnivå mot todo.completedItems.0 har ingen verdi å sjekke mot. Tapte handlinger: todo.clearCompleted.' }] },
        previewCaption: 'Forhåndsvisning av forrige gyldige utkast.' }) },
  { name: 'felles-utkast-konflikt', preview: true, state: base(
      { description: 'Et panel som viser gjøremålene mine med frist, og lar meg krysse dem av. Vis de fullførte under.', modelText: 'Modell: Mistral Small (EU), via tilgangen din.', messages: [] },
      { reachability: { summary: 'Sjekket: alle elementer kan vises. 1 handling kan nås: todo.toggleTodo.', findings: [] },
        previewCaption: 'Forhåndsvisning av utkastet med dine egne data.',
        coedit: { editors, revisionText: 'Du redigerer revisjon 4. Siste lagrede er revisjon 5.',
          conflicts: [{ title: 'Ola lagret en nyere versjon 14:07', text: 'Endringen din bygger på revisjon 4 og ble ikke lagret. Hent siste versjon, så ligger endringen din klar til å legges inn på nytt.' }],
          inviteDraft: '' } }) },
  { name: 'hjelper-flate', skeleton: 'helper', state: { workbenchHelper: { state: { messages: [
      { role: 'Du', text: 'Lag en flate som viser oppgavene mine' },
      { role: 'Hjelper', text: 'Settet «Denne flaten» kan bare flytte oppgaver mellom faner. Å lage en flate gjøres i settet «Flater og GUI», som bruker Cell Configuration Studio. Bytt sett, eller åpne Studio direkte.' }] } } } }
];
const helperSkeleton = { VStack: { spacing: 12, elements: [
  { Text: { text: 'Hjelper · sett «Denne flaten»', modifiers: { styleRole: 'title' } } },
  { List: { keypath: 'workbenchHelper.state.messages', flowElementSkeleton: { VStack: { elements: [
    { Text: { keypath: 'role', modifiers: { styleRole: 'headline' } } }, { Text: { keypath: 'text' } } ] } } } },
  { HStack: { spacing: 8, wrap: true, elements: [
    { Button: { keypath: 'workbenchHelper.selectSet', label: 'Bytt til «Flater og GUI»', payload: 'other-surfaces' } },
    { Button: { keypath: 'workbenchHelper.openStudio', label: 'Åpne Studio' } } ] } }
] } };
module.exports = { all, helperSkeleton };
