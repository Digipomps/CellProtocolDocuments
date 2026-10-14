// Vektmodellen fra WP3 (PalazzoWeightPolicy + PalazzoSignalGraphMatcher), gjengitt for siden.
const ARTICLES = {
  "art-arancini": {t:"Arancini", tags:["arancini","catania","fritert","gatemat","palermo","ris","safran"]},
  "art-cannoli": {t:"Cannoli", tags:["cannoli","dessert","fritert","kandisert","palermo","pistasj","ricotta"]},
  "art-caponata": {t:"Caponata", tags:["agrodolce","antipasto","aubergine","caponata","kapers","oliven","vegetar"]},
  "art-etna-vin": {t:"Etna-vin", tags:["carricante","etna","hvitvin","nerello mascalese","rødvin","vin","vulkan"]},
  "art-granita": {t:"Granita", tags:["brioche","dessert","frokost","granita","kaffe","mandel","messina","sitron"]},
  "art-pasta-alla-norma": {t:"Pasta alla Norma", tags:["aubergine","basilikum","catania","norma","pasta","ricotta salata","tomat"]},
  "art-pasta-con-le-sarde": {t:"Pasta con le sarde", tags:["bucatini","fennikel","fisk","palermo","pasta","rosiner","safran","sardiner"]},
  "art-pistasj-bronte": {t:"Pistasj fra Bronte", tags:["bronte","dop","etna","gelato","nøtter","pesto","pistasj"]}
};
const R = {W:"wantToTaste", I:"interesting", N:"notForMe"};
const GUESTS = [
  {name:"Ombestemmer seg", formaal:"Vil få beslektet matinnhold etter at hun likevel vil smake caponata.",
   taps:[["art-caponata","I"],["art-caponata","N"],["art-caponata","W"]], skalFaa:["art-pasta-alla-norma"], skalIkkeFaa:["art-caponata"], ref:[]},
  {name:"Palermo, men ikke fritert", formaal:"Vil oppdage mer fra Palermo uten å få tilbud om fritert mat.",
   taps:[["art-arancini","I"],["art-cannoli","N"]], skalFaa:["art-pasta-con-le-sarde"], skalIkkeFaa:["fritert"], ref:["art-pasta-alla-norma"]},
  {name:"Vegetar", formaal:"Vil oppdage vegetarisk mat og unngå tilbud med fisk eller kjøtt.",
   taps:[["art-caponata","W"],["art-pasta-con-le-sarde","N"]], skalFaa:["art-pasta-alla-norma"], skalIkkeFaa:["fisk","sardiner","art-arancini"], ref:[]},
  {name:"Trykker mye «Interessant»", formaal:"Vil fortsette å oppdage innhold etter mange ulike Interessant-trykk.",
   taps:[["art-arancini","I"],["art-caponata","I"],["art-pasta-alla-norma","I"],["art-pistasj-bronte","I"],["art-granita","I"]],
   skalFaa:["art-cannoli","art-etna-vin","art-pasta-con-le-sarde"], skalIkkeFaa:["art-arancini","art-caponata","art-pasta-alla-norma","art-pistasj-bronte","art-granita"],
   ref:["art-arancini","art-cannoli","art-caponata","art-etna-vin","art-pasta-alla-norma","art-pasta-con-le-sarde"]},
  {name:"Bare «Ikke for meg»", formaal:"Vil slippe tilbud som bygger på hennes avvisninger alene.",
   taps:[["art-arancini","N"],["art-cannoli","N"],["art-pasta-con-le-sarde","N"]], skalFaa:[], skalIkkeFaa:Object.keys(ARTICLES), ref:[]},
  {name:"Samme knapp flere ganger", formaal:"Vil få beslektet innhold når hun gjentar at hun vil smake caponata.",
   taps:[["art-caponata","W"],["art-caponata","W"],["art-caponata","W"]], skalFaa:["art-pasta-alla-norma"], skalIkkeFaa:["art-caponata"], ref:["art-pasta-alla-norma"]},
  {name:"Ett «Interessant»-trykk", formaal:"Vil få minst ett beslektet tilbud etter ett eneste Interessant-trykk.",
   taps:[["art-caponata","I"]], skalFaa:["art-pasta-alla-norma"], skalIkkeFaa:["art-caponata"], ref:["art-pasta-alla-norma"]}
];
function isMonotone(p){ return p.interesting + p.reinforce*(p.cap - p.interesting) <= p.wantToTaste + 1e-12; }
function run(guest, p){
  const st = {};
  for (const [a, r] of guest.taps){
    const prev = st[a];
    const n = prev && prev.r === r ? prev.n + 1 : 0;
    const base = p[R[r]];
    const goal = base + p.reinforce*(p.cap - base)*n/(n+1);
    const m = prev ? prev.m + p.approach*(goal - prev.m) : goal;
    st[a] = {r, n, m};
  }
  const offers = [], closed = [];
  for (const [a, v] of Object.entries(st)) if (v.r === "N") closed.push(a);
  for (const c of Object.keys(ARTICLES)){
    if (st[c]) continue;
    const tc = ARTICLES[c].tags; let s = 0, hit = false, parts = [];
    for (const [a, v] of Object.entries(st)){
      const ov = ARTICLES[a].tags.filter(x => tc.includes(x));
      if (!ov.length) continue; hit = true;
      const sign = v.r === "N" ? -1 : 1;
      const contrib = sign * v.m * ov.length / tc.length * (sign < 0 ? p.negativeScale : 1);
      s += contrib; parts.push({from:a, r:v.r, tags:ov, contrib});
    }
    if (hit && s >= p.threshold) offers.push({id:c, sum:s, parts});
  }
  offers.sort((x,y) => y.sum - x.sum || (x.id < y.id ? -1 : 1));
  closed.sort();
  return {offers, closed, state: st};
}
function judge(guest, res){
  const ids = res.offers.map(o => o.id);
  const faaOk = guest.skalFaa.length === 0 || guest.skalFaa.some(x => ids.includes(x));
  const brudd = [];
  for (const o of res.offers) for (const x of guest.skalIkkeFaa)
    if (o.id === x || ARTICLES[o.id].tags.includes(x)) brudd.push(o.id + (o.id === x ? "" : " (" + x + ")"));
  const rodt = ids.length === 0 && guest.ref.length > 0;
  return {ok: faaOk && brudd.length === 0, faaOk, brudd, rodt};
}
if (typeof module !== "undefined") module.exports = {ARTICLES, GUESTS, run, judge, isMonotone};
