// Review-only fixture harness. No network, storage writes, jobs or deletion.
const txt = (text, modifiers) => ({ Text: { text, ...(modifiers ? {modifiers} : {}) } });
const val = keypath => ({Text:{keypath}});
const v = elements => ({VStack:{elements,spacing:10}});
const h = elements => ({HStack:{elements,spacing:12}});
const section = (title,content) => ({Section:{header:txt(title),content}});
const picker = (label,key) => ({Picker:{label,keypath:`options.${key}`,optionLabelKeypath:'label',selectionValueKeypath:'id',selectionStateKeypath:`filters.${key}`,selectionActionKeypath:`preview.filter.${key}`,selectionPayloadMode:'item_id',allowsEmptySelection:false}});
const files = [
 {id:'cache',title:'SwiftPM · delt byggcache',path:'arbeidsrom/cache/swiftpm',machine:'mac',project:'scaffold',status:'active',meta:'Laptop · CellScaffold · 2,4 GiB',reason:'Aktiv — brukes av to registrerte byggjobber.',origin:'Opphav: byggjobb eksempel-42 · Codex',retention:'Beholdes mens én eller flere jobber bruker cachen.',size:'2,4 GiB · eget filsystem på laptop'},
 {id:'report',title:'Testrapport · avsluttet jobb',path:'arbeidsrom/eksempel-41/testresultat',machine:'mac',project:'agent',status:'retained',meta:'Laptop · HavenAgentD · 12 MiB',reason:'Beholdes — dokumenterer en åpen PR.',origin:'Opphav: agentjobb eksempel-41 · Claude',retention:'Beholdes så lenge PR-en trenger testbeviset.',size:'12 MiB · eget filsystem på laptop'},
 {id:'old',title:'Gammelt bygg · ukjent opphav',path:'arbeidsrom/eldre-bygg',machine:'host',project:'scaffold',status:'unknown',meta:'Vert · CellScaffold · størrelse ikke verifisert',reason:'Ukjent — mangler opprettelsesbevis og referansekontroll.',origin:'Opphav: ukjent · ikke utledet fra mappenavn',retention:'Kan ikke vurderes for sletting før opphav og bruk er kontrollert.',size:'Ukjent · vertens rotdisk'},
 {id:'candidate',title:'Midlertidige produkter · avsluttet jobb',path:'arbeidsrom/eksempel-39/produkter',machine:'host',project:'scaffold',status:'review',meta:'Vert · CellScaffold · 640 MiB',reason:'Kan vurderes — utløpt bevaring, ingen aktive avhengigheter i eksemplet.',origin:'Opphav: byggjobb eksempel-39 · Codex',retention:'Ryddeforslag krever fersk kontroll og separat godkjenning.',size:'640 MiB · vertens rotdisk'}
];
const choice=(id,label)=>({id,label});
const initial = () => ({
 activeTab:'files',tabs:[choice('files','Filer og mapper'),choice('graph','Relasjoner'),choice('retention','Bevaring')].map(x=>({id:x.id,title:x.label})),
 filters:{machine:'all',project:'all',status:'all'},
 options:{machine:[choice('all','Begge maskiner'),choice('mac','Laptop'),choice('host','Vert')],project:[choice('all','Alle prosjekter'),choice('scaffold','CellScaffold'),choice('agent','HavenAgentD')],status:[choice('all','Alle tilstander'),choice('active','Aktiv'),choice('retained','Beholdes'),choice('review','Kan vurderes'),choice('unknown','Ukjent')]},
 rows:files,selectedID:'cache',selected:files[0],message:'4 eksempler · bare registrerte jobbområder',
 coverage:'Dekning: registrerte jobber. Filer med ukjent opphav vises uten tilordnet agent.',
 graph:{title:'Eksempel · hvorfor cachen beholdes',nodes:[
 {id:'p',label:'CellScaffold',kind:'Prosjekt',x:130,y:100,color:'#86b8ff'},
 {id:'j1',label:'Codex · bygg 42',kind:'Jobb',x:350,y:70,color:'#b9a7ff'},
 {id:'j2',label:'Claude · bygg 43',kind:'Jobb',x:350,y:280,color:'#b9a7ff'},
 {id:'f',label:'SwiftPM-cache',kind:'Mappe',x:560,y:160,color:'#f1c773'},
 {id:'d',label:'Laptop · disk',kind:'Filsystem',x:780,y:120,color:'#8ed7c6'}
 ],edges:[{source:'j1',target:'p',label:'tilhører'},{source:'j2',target:'p',label:'tilhører'},{source:'j1',target:'f',label:'opprettet'},{source:'j2',target:'f',label:'bruker'},{source:'f',target:'d',label:'ligger på'}]}
});
const skeleton=v([
 section('Developer Workbench',[txt('Filer, opphav og bevaring'),txt('FORHÅNDSVISNING · Eksempeldata. Ingen innsamler eller grafdatabase er koblet til.')]),
 {Tabs:{tabsKeypath:'tabs',activeTabStateKeypath:'activeTab',selectionActionKeypath:'preview.tab',panels:[
 {id:'files',content:[
 section('Filer og mapper',[h([picker('Maskin','machine'),picker('Prosjekt','project'),picker('Tilstand','status')]),val('message'),val('coverage'),
 {List:{keypath:'rows',flowElementSkeleton:v([val('title'),val('meta'),val('reason'),{Button:{keypath:'preview.details',label:'Vis detaljer',payloadKeypath:'id'}}])}}]),
 section('Valgt fil eller mappe',[val('selected.title'),val('selected.path'),val('selected.origin'),val('selected.size'),val('selected.retention')])
 ]},
 {id:'graph',content:[section('Relasjoner',[txt('SwiftPM-cache · relasjoner i utvalget'),txt('CellScaffold ← tilhører ← Codex · bygg 42'),txt('Codex · bygg 42 → opprettet → SwiftPM-cache'),txt('Claude · bygg 43 → bruker → SwiftPM-cache'),txt('SwiftPM-cache → ligger på → Laptop · disk'),{Button:{keypath:'preview.openCache',label:'Vis cachen i filoversikten'}}]),section('Hvorfor beholdes dette?',[txt('To jobber er koblet til den samme cachen. Avslutning av én jobb frigir ikke den andre jobbens avhengighet.'),txt('Eksempeldata — relasjonene kommer fra lokale fixtures. Live GraphStore-tilkobling må implementeres.')])]},
 {id:'retention',content:[section('Bevaring og ryddeforslag',[
 txt('Aktiv — en jobb, prosess, mount eller lease bruker artefakten.'),txt('Beholdes — bevis, kildekode eller en avhengighet trenger den fortsatt.'),txt('Kan vurderes — bevaringen er utløpt og de aktuelle kontrollene er bestått.'),txt('Ukjent — mangler grunnlag. Opphav og bruk må undersøkes.'),
 txt('En utløpt frist gir et forslag. Aktiv bruk, uavklarte avhengigheter og beskyttede data hindrer sletting.'),txt('Tid og bevaringsgrunn knyttes til hvert artefakt. Utførelse følger eksisterende rydderutine med ferske kontroller og godkjenning.')])]}]}}
]);
window.reviewSkeleton=skeleton;
let data=initial();let mode='filled';window.reviewActions=[];
const renderer=window.HavenSkeletonRuntime.createRenderer({rootElement:document.getElementById('porthole-skeleton-root'),skeleton,onAction:async(key,payload)=>{
 window.reviewActions.push({key,payload});
 if(key==='preview.tab')data.activeTab=payload.selectedValue||payload.id;
 if(key.startsWith('preview.filter.')){data.filters[key.split('.').at(-1)]=payload.selectedValue||payload.selected;filter();}
 if(key==='preview.select'){data.selectedID=payload.selectedValue||payload.selected;data.selected=files.find(x=>x.id===data.selectedID)||data.selected;}
 if(key==='preview.details'){const id=typeof payload==='string'?payload:payload.id;data.selectedID=id;data.selected=files.find(x=>x.id===id)||data.selected;}
 if(key==='preview.openCache'){data.activeTab='files';data.filters={machine:'all',project:'all',status:'all'};filter();data.selectedID='cache';data.selected=files[0];}
 if(key==='preview.node')data.graphSelection='Valgt relasjonspunkt: '+(payload.label||payload.id||'ukjent');
 renderer.update(data);return {status:'ok'};
}});
function filter(){data.rows=mode==='filled'?files.filter(x=>Object.entries(data.filters).every(([k,v])=>v==='all'||x[k]===v)):[];data.message=mode==='empty'?'Ingen registrerte artefakter ennå.':mode==='error'?'Oppdatering utilgjengelig. Siste observasjon kan ikke brukes til rydding.':`${data.rows.length} eksempler i utvalget`;if(!data.rows.some(x=>x.id===data.selectedID)){data.selectedID=data.rows[0]?.id||'';data.selected=data.rows[0]||{title:mode==='error'?'Ingen fersk observasjon':'Ingen fil valgt',path:'',origin:'',size:'',retention:mode==='error'?'Prøv igjen når forbindelsen er tilbake.':'Nye filer vises når en registrert jobb rapporterer metadata.'};}}
window.setReviewMode=next=>{mode=next;data=initial();if(next==='empty')data.coverage='Start en registrert jobb for å få oversikt. Ingen generell skanning er aktiv.';if(next==='error')data.coverage='Forbindelsen til grafen er nede. Lokale registreringer skal vente på synkronisering.';filter();renderer.update(data);};
document.getElementById('review-state').onchange=e=>window.setReviewMode(e.target.value);
document.getElementById('review-theme').onchange=e=>document.documentElement.dataset.workbenchTheme=e.target.value;
window.setReviewMode('filled');
