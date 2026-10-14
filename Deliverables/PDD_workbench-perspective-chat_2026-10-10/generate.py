"""P1-GUI design fixtures; no live reads, model calls, jobs or writes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'skeleton'
OUT.mkdir(exist_ok=True)
P = {}
PALETTES = {
    'light': dict(bg='#f5f5f7', surface='#ffffff', sidebar='#ececef', text='#1d1d1f', muted='#62626b',
                  border='#d4d4db', accent='#0068d6', selection='#deebff', accentText='#174c90',
                  good='#216343', warn='#805516', subtle='#f0f0f3'),
    'dark': dict(bg='#1c1c1f', surface='#29292d', sidebar='#242427', text='#f5f5f7', muted='#b5b5bf',
                 border='#45454c', accent='#086cde', selection='#193b60', accentText='#d1e6ff',
                 good='#a1dfb9', warn='#f0cc8a', subtle='#323237'),
}

def node(kind, **kw): return {kind: kw}
def v(*children, gap=12, **m):
    return node('VStack', elements=list(children), spacing=gap, modifiers=dict(hAlignment='leading', **m))
def h(*children, gap=12, responsive=False, **m):
    if responsive: m['layoutVariants'] = [dict(maxAvailableWidth=700, axis='vertical')]
    m['styleClasses'] = ['helper-layout-row'] + m.get('styleClasses', [])
    return node('HStack', elements=list(children), spacing=gap, modifiers=dict(vAlignment='top', wrap=False, **m))
def t(text=None, key=None, size=14, weight='regular', color=None, **m):
    return node('Text', **({'keypath': key} if key else {'text': text}),
                modifiers=dict(fontSize=size, fontWeight=weight, foregroundColor=color or P['text'], **m))
def b(label, action, payload=None, primary=False, **m):
    modifiers=dict(fontSize=13, fontWeight='medium', background=P['accent'] if primary else P['surface'],
                   foregroundColor='#ffffff' if primary else P['text'], cornerRadius=8,
                   borderWidth=1, borderColor=P['accent'] if primary else P['border'])
    modifiers.update(m)
    if primary: modifiers['styleClasses']=['primary-action']
    opts = dict(label=label, keypath='helper.'+action,
                modifiers=modifiers)
    if payload is not None: opts['payload'] = payload
    return node('Button', **opts)
def bound_button(label, action, payload_key, primary=False):
    n = b(label, action, primary=primary); n['Button']['payloadKeypath'] = payload_key
    return n
def card(*children, **m):
    return v(*children, padding=18, background=P['surface'], cornerRadius=12,
             borderWidth=1, borderColor=P['border'], **m)
def pill(label, color=None):
    return t(label, size=12, weight='medium', color=color or P['accentText'], padding=6,
             background=P['selection'], cornerRadius=6)
def field(source, target, placeholder):
    return node('TextField', sourceKeypath=source, targetKeypath='helper.'+target, placeholder=placeholder,
                modifiers=dict(fontSize=14, foregroundColor=P['text'], background=P['surface'],
                               cornerRadius=8, borderWidth=1, borderColor=P['border'], maxWidthInfinity=True))
def area(source, target, placeholder, lines=3):
    return node('TextArea', sourceKeypath=source, targetKeypath='helper.'+target, placeholder=placeholder,
                minLines=lines, maxLines=10, submitOnEnter=False, editorMode='plain',
                modifiers=dict(fontSize=14, foregroundColor=P['text'], background=P['surface'],
                               padding=10, cornerRadius=8, borderWidth=1, borderColor=P['border'], maxWidthInfinity=True))
def picker(label, items, selected, action):
    return node('Picker', label=label, keypath=items, optionLabelKeypath='title', selectionValueKeypath='id',
                selectionStateKeypath=selected, selectionActionKeypath='helper.'+action,
                selectionPayloadMode='item_id', allowsEmptySelection=False,
                modifiers=dict(fontSize=13, foregroundColor=P['text'], background=P['surface'], cornerRadius=6))
def rows(key, *children):
    return node('List', keypath=key, selectionMode='none', flowElementSkeleton=v(*children, gap=8),
                modifiers=dict(maxWidthInfinity=True,styleClasses=['helper-rows']))
def mount(key, instance):
    return node('ComponentSurface', sourceKeypath=key, instanceID=instance, variant='inline',
                modifiers=dict(maxWidthInfinity=True))

def helper():
    return card(
        h(v(t('Hjelpechat', size=20, weight='semibold'), t(key='sessionLabel', size=12, color=P['muted']), gap=3, flexGrow=1),
          b('Historikk', 'openHistory', {'scope':'private'})),
        picker('Perspektiv', 'perspectives', 'selectedPerspective', 'selectPerspective'),
        picker('Modell', 'models', 'selectedModel', 'selectModel'),
        t(key='recipientLabel', size=12, color=P['muted']),
        h(pill('Privat samtale'), b('Kontekst', 'inspectContext'), b('Pakker', 'openPackages'), gap=8),
        t(key='contextSummary', size=12, color=P['muted']),
        rows('notices', t(key='title', weight='semibold', color=P['warn']), t(key='body', size=13)),
        rows('messages', t(key='speaker', size=12, weight='semibold', color=P['muted']), t(key='text', size=14)),
        rows('proposals',
             t(key='title', size=15, weight='semibold'), t(key='summary', size=13),
             t(key='scope', size=12, color=P['muted']),
             h(bound_button('Legg i kø', 'enqueue', 'command', True),
               bound_button('Se arbeidsordre', 'inspectProposal', 'id'), gap=8)),
        rows('blocked', t(key='title', weight='semibold', color=P['warn']), t(key='reason', size=13),
             bound_button('Se krav', 'inspectRequirements', 'command')),
        rows('starters', t(key='title', weight='semibold'), t(key='body', size=13),
             bound_button('Utforsk idé', 'useStarter', 'id')),
        area('draft', 'setDraftMessage', 'Skriv en melding …', 2),
        h(v(t(key='eventStatus', size=11, color=P['muted']), gap=0, flexGrow=1),
          bound_button('Send', 'send', 'sendCommand', True)),
        gap=12)

PERSPECTIVES = [dict(id=i, title=n) for i,n in [
    ('ideas','Idéutvikling'),('surfaces','CellConfiguration og flater'),('purpose','Formålstrær'),
    ('agreement','Agreement og tilgang'),('delivery','Fra idé til produksjon'),('mine','Min prosjektassistent')]]
MODELS = [dict(id='local-fixture',title='Lokal modell'),dict(id='openai-fixture',title='OpenAI · tillatt rute'),
          dict(id='anthropic-fixture',title='Anthropic · tillatt rute')]

def helper_state(kind='filled', session='demo-session-01', draft=''):
    s = dict(sessionID=session, sessionLabel='CellScaffold · ny arbeidsøkt', perspectives=PERSPECTIVES,
             selectedPerspective='delivery', models=MODELS, selectedModel='local-fixture',
             recipientLabel='Mottaker: lokal modell · innholdet forblir lokalt',
             contextSummary='Kontekst: DEMO-014 · prosjektets README · 2 valgte kildeutdrag',
             messages=[], notices=[], proposals=[], blocked=[], starters=[], draft=draft,
             eventStatus='Oppdatert fra hendelser · nå',
             sendCommand=dict(sessionID=session,expectedRevision=12,commandID='demo-send-'+session))
    if kind == 'empty':
        s.update(selectedPerspective='ideas',contextSummary='Ingen prosjektdata er lagt til i samtalen.',
                 sessionLabel='Ny privat samtale', eventStatus='Klar for en ny samtale')
        s['starters'] = [dict(id='demo-starter',title='Hva vil du utforske?',
                             body='Start med en idé. Hjelperen stiller spørsmål og samler neste steg.')]
    else:
        s['messages'] = [dict(id='m1',speaker='DU',text='Gjør denne ideen klar for en agentjobb.'),
                         dict(id='m2',speaker='HJELPER · LOKAL MODELL',text='Jeg foreslår å avgrense jobben til å rette tilbakeknappen og teste at riktig arbeidsflate gjenåpnes.')]
        if kind == 'filled':
            s['proposals'] = [dict(id='demo-proposal-01',title='Forslag til arbeidsordre',
                summary='Rett tilbakeknappen i prosjektporteføljen. Kjør lokal navigasjonstest før PR.',
                scope='Codex · CellScaffold · isolert arbeidskopi · maks 20 min',
                command=dict(proposalID='demo-proposal-01',sessionID=session,expectedRevision=12,commandID='demo-queue-'+session))]
    if kind == 'error':
        s.update(eventStatus='Frakoblet · siste oppdatering 10:42')
        s['notices']=[dict(title='Venter på forbindelse',body='Utkastet er bevart. Status hentes inn igjen når forbindelsen er tilbake.')]
        s['blocked']=[dict(id='demo-command-02',title='Uavklart køstatus',reason='Forbindelsen brøt etter sending. Les status for samme ordre før et nytt forsøk.',
                          label='Les køstatus',keypath='helper.readCommandStatus',command={'commandID':'demo-command-02'})]
    if kind == 'blocked':
        s['blocked']=[dict(id='demo-merge-01',title='Merge er ikke tilgjengelig ennå',reason='PR #DEMO har en feilet navigasjonstest. Ny kontroll og gjeldende head kreves før merge.',command={'proposalID':'demo-merge-01'})]
    if kind=='external':
        s.update(selectedModel='openai-fixture',recipientLabel='Mottaker: OpenAI · eksempelmodell A · ekstern tjeneste',
                 contextSummary='Valgt for sending: oppgavetittel og to offentlige kildeutdrag. Private notater er utelatt.',
                 messages=[],eventStatus='Venter på gjennomgang av datagrunnlaget')
        s['notices']=[dict(title='Se hva modellen får',body='Gjennomgå de valgte utdragene under Kontekst før første sending til denne tjenesten.')]
    return s

def mount_value(component, state):
    return dict(componentID='haven.workbench.helper.candidate',revision='gui-v1',
                sourceCellEndpoint='cell:///WorkbenchHelper',skeleton=component,item=state)

def header(title, subtitle, admin=False):
    return h(v(t(title,size=25,weight='semibold'),t(subtitle,size=13,color=P['muted']),gap=4,flexGrow=1),
             b('Admin Workbench' if not admin else 'Developer Workbench','openAdmin' if not admin else 'openDeveloper'),
             responsive=True,padding=22,background=P['surface'])

def sidebar(selected='Arbeidsrom'):
    return v(t('WORKBENCH',size=11,weight='semibold',color=P['muted']),
             *[b(name,'navigate',{'surface':key},styleClasses=['helper-nav','helper-nav-selected'] if name==selected else ['helper-nav'],maxWidthInfinity=True)
               for name,key in [('Arbeidsrom','workspace'),('Alle prosjekter','projects'),('Ideer','ideas'),
                                ('Board','board'),('Agentjobber','jobs'),('Historikk','history'),('Perspektiver','packages')]],
             t('MINE VERKTØY',size=11,weight='semibold',color=P['muted']),
             b('Åpne selvstendig chat','openStandalone'),
             padding=18,background=P['sidebar'],
             layoutVariants=[dict(minAvailableWidth=701,width=196),dict(maxAvailableWidth=700,hidden=True)])

def task_context():
    return v(
        h(v(t('CellScaffold',size=25,weight='semibold'),t('Arbeidsrom  /  DEMO-014',color=P['muted']),gap=5,flexGrow=1),
          b('Alle prosjekter','navigate',{'surface':'projects'}),responsive=True),
        card(h(pill('Klar for arbeid'),pill('Formål: sammenhengende navigasjon'),responsive=True),
             t('Tilbake skal føre til riktig arbeidsflate',size=22,weight='semibold'),
             t('Fra prosjektporteføljen skal jeg komme tilbake til Developer Workbench uten å miste valgt prosjekt.'),
             t('AKSEPTKRITERIER',size=11,weight='semibold',color=P['muted']),
             t('• Riktig arbeidsflate og prosjekt åpnes\n• Direkte lenke og tilbakeknapp fungerer\n• Testen kjøres lokalt før PR'),
             h(b('Les repo','readRepo',{'projectID':'demo-cellscaffold'}),
               b('Utfør prompt','prepareAgentJob',{'workItemID':'DEMO-014'}),responsive=True)),
        card(t('Fra idé til produksjon',size=17,weight='semibold'),
             t('Idé  →  Oppgave  →  Agentjobb  →  PR  →  Deploy',size=13,color=P['accentText']),
             t('Neste steg: legg en avgrenset arbeidsordre i kø.',size=13),
             t('Deploy styres i Admin Workbench.',size=12,color=P['muted'])),
        card(t('Siste hendelser',size=17,weight='semibold'),
             t('10:42   Oppgaven ble satt til Klar\n10:39   Akseptkriterier ble lagt til\n10:34   Idé ble knyttet til prosjektet',size=13),
             b('Åpne historikk','openHistory',{'workItemID':'DEMO-014'})),
        gap=18, flexGrow=1)

def screen(inner):
    return v(inner, gap=0, background=P['bg'],foregroundColor=P['text'],minHeight=820)
def workbench(component):
    return screen(v(header('Developer Workbench','Ditt arbeidsrom for ideer, utvikling og leveranser'),
        h(sidebar(),h(task_context(),v(mount('chat','workbench-helper'),
           layoutVariants=[dict(minAvailableWidth=701,width=440),dict(maxAvailableWidth=700,width=342)],gap=0),
           responsive=True,padding=22,gap=22,flexGrow=1),responsive=True,gap=0),gap=0))

def standalone():
    return screen(v(header('Hjelpechat','Perspektiv, modell og kontekst for arbeidet ditt'),
        v(mount('chat','standalone-helper'),layoutVariants=[dict(minAvailableWidth=800,width=760)],padding=24,gap=0),gap=0))

def butler():
    return screen(v(header('Butler','Samtaler og verktøy samlet'),
        h(v(card(t('Samtalen din',size=20,weight='semibold'),
                     t('DU',size=12,color=P['muted']),t('La oss jobbe med navigasjonsfeilen i CellScaffold.'),
                     t('BUTLER',size=12,color=P['muted']),t('Jeg har åpnet Hjelpechat med oppgaven som kontekst.'),
                     b('Åpne i Developer Workbench','openDeveloper',{'sessionID':'demo-session-01'})),
               card(t('Aktivt verktøy',size=16,weight='semibold'),t('Hjelpechat · CellScaffold',size=13),
                    t('Samme samtale kan åpnes i eget vindu.',size=12,color=P['muted'])),flexGrow=1),
          v(mount('chat','butler-helper'),layoutVariants=[dict(minAvailableWidth=701,width=480),dict(maxAvailableWidth=700,width=342)],gap=0),
          responsive=True,padding=24,gap=24),gap=0))

def package_editor():
    return screen(v(header('Perspektivpakker','Velg et arbeidssett eller lag ditt eget'),
        h(sidebar('Perspektiver'),
          v(t('Bibliotek',size=20,weight='semibold'),
            *[b(x['title'],'inspectPackage',x['id']) for x in PERSPECTIVES],
            b('Ny pakke','newPackage',primary=True),
            t('Pakken gir kontekst. Tilgang styres av dine avtaler og roller.',size=12,color=P['muted']),
            width=280,padding=22),
          v(card(h(v(t(key='package.titleLabel',size=22,weight='semibold'),
                          t(key='package.versionLabel',size=12,color=P['muted']),gap=4,flexGrow=1),
                       pill('Utkast'),responsive=True),
                 rows('package.notices',t(key='title',weight='semibold'),t(key='body',size=13),
                      b('Sammenlign versjoner','packageDiff',{'packageID':'demo-mine'})),
                 field('package.title','setPackageTitle','Pakkens navn'),
                 picker('Formål','package.purposes','package.purpose','setPackagePurpose'),
                 t('Instruksjoner',weight='semibold'),
                 area('package.instructions','setPackageInstructions','Hva skal hjelperen gjøre?',4),
                 t('Skills',weight='semibold'),
                 t(key='package.skillsLabel',size=13,color=P['muted']),
                 b('Velg skills','chooseSkills'),
                 t('Kontekst',weight='semibold'),t(key='package.contextLabel',size=13,color=P['muted']),
                 b('Velg kontekst','chooseContext'),
                 t('Modell og databruk',weight='semibold'),
                 t('Lokal modell er standard. Før ekstern bruk vises mottaker og hvilke utdrag som sendes.',size=13),
                 h(b('Lagre ny versjon','savePackage',{'packageID':'demo-mine','expectedRevision':3},primary=True),
                   b('Se endringer','packageDiff',{'packageID':'demo-mine'}),responsive=True),
                 b('Del lagret versjon …','preparePackageShare',{'packageID':'demo-mine','version':3}),
                 t('En pågående svartur beholder pakken den startet med.',size=12,color=P['muted'])),padding=22,flexGrow=1),
          responsive=True,gap=0),gap=0))

def history():
    return screen(v(header('Historikk','Finn hendelser, kilder og tidligere arbeid'),
        h(sidebar('Historikk'),v(
            h(picker('Omfang','history.scopes','history.scope','setHistoryScope'),
              picker('Søk etter','history.modes','history.mode','setHistoryMode'),responsive=True),
            h(v(field('history.query','setHistoryQuery','Søk i historikken …'),flexGrow=1),
              b('Søk','searchHistory',{'queryID':'demo-history-query'},primary=True),responsive=True),
            t(key='history.scopeLabel',size=13,color=P['muted']),
            rows('history.notices',t(key='title',size=19,weight='semibold'),t(key='body')),
            rows('history.results',t(key='title',size=19,weight='semibold'),t(key='provenance',size=12,color=P['muted']),
                 t(key='excerpt'),t(key='relations',size=13),
                 h(bound_button('Åpne kilde','openSource','id'),bound_button('Lag oppfølging','followUp','id'),
                   bound_button('Velg utdrag å dele','prepareShare','id'),responsive=True)),
            t('Å åpne en gammel hendelse utfører ikke handlingen på nytt.',size=12,color=P['muted']),
            padding=24,flexGrow=1),responsive=True,gap=0),gap=0))

def two_mounts():
    return screen(v(header('To uavhengige samtaler','Komponentprøve · egne utkast og egne arbeidsøkter'),
        h(v(mount('chat','mount-A'),flexGrow=1),v(mount('chatB','mount-B'),flexGrow=1),
          responsive=True,padding=24),gap=0))

def context_editor():
    return screen(v(header('Kontekst og skills','Velg akkurat det hjelperen trenger for denne arbeidsøkten'),
        v(card(t('Formål: sammenhengende navigasjon',size=20,weight='semibold'),
               t('Tilgjengelige skills',weight='semibold'),
               rows('context.skills',t(key='title',weight='semibold'),t(key='detail',size=13),
                    bound_button('Velg','toggleSkill','id')),
               t('Kontekstkilder',weight='semibold'),
               rows('context.sources',t(key='title',weight='semibold'),t(key='detail',size=13),
                    bound_button('Velg','toggleContextSource','id')),
               t('En skill eller en kilde gir aldri nye rettigheter.',size=12,color=P['muted']),
               b('Se datagrunnlag før sending','reviewModelContext',{'sessionID':'demo-session-01'},primary=True)),
          padding=24),gap=0))

def share_preview():
    return screen(v(header('Del en pakkeversjon','Gjennomgå versjon og publikum før deling'),
        v(card(t('Min prosjektassistent · versjon 3',size=23,weight='semibold'),
               picker('Publikum','review.audiences','review.audience','selectShareAudience'),
               t('Dette blir delt',weight='semibold'),
               t('Instruksjonene i versjon 3 · valgte skill-referanser · referanse til prosjektets README'),
               t('Private notater, samtaler og personlige kontekstkilder er utelatt.',size=13),
               t('Mottakerne bruker sine egne rettigheter når de åpner kildene.',size=13,color=P['muted']),
               rows('review.notices',t(key='title',weight='semibold'),t(key='body')),
               rows('review.actions',b('Del versjon','sharePackageVersion',primary=True)),
               b('Behold privat','cancelShare',{'packageID':'demo-mine'})),padding=24),gap=0))

def model_preview():
    return screen(v(header('Datagrunnlag for modellen','Se mottaker, modell og valgte utdrag'),
        v(card(t('OpenAI · eksempelmodell A',size=23,weight='semibold'),
               pill('Ekstern tjeneste'),
               t('Samtalen lagres privat. Valgt innhold sendes til denne tjenesten ved utføring.',size=14),
               t('Valgt innhold',weight='semibold'),
               t('DEMO-014: Tilbake skal føre til riktig arbeidsflate\n\nKildeutdrag 1: Prosjektporteføljen har en lenke tilbake til arbeidsrommet.\nKildeutdrag 2: Valgt prosjekt identifiseres med prosjekt-ID.'),
               t('Kilder: eksempeloppgave + offentlige repo-utdrag. Ingen private notater eller historikk er valgt.',size=12,color=P['muted']),
               rows('review.notices',t(key='title',weight='semibold'),t(key='body')),
               rows('review.actions',b('Bruk valgt innhold','confirmModelContext',primary=True)),
               b('Endre utvalg','inspectContext',{'sessionID':'demo-session-01'}),
               b('Velg lokal modell','useLocalModel',{'sessionID':'demo-session-01'})),padding=24),gap=0))

def config(skeleton, title):
    return dict(uuid='fc9fb625-0d01-4c65-b3a3-b787e8e52101', name='P1-GUI · '+title,
                description='Designkandidat med syntetiske data. Nye Explore-kontrakter er ikke implementert.',
                cellReferences=[dict(endpoint='cell:///WorkbenchHelper',label='helper',subscribeFeed=True)],
                skeleton=skeleton)

def save(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

shots=[]
for theme in PALETTES:
    P=PALETTES[theme]
    component=helper()
    save(f'helper-{theme}.skeleton.json',component)
    for surface, builder, kinds in [
        ('workbench',lambda:workbench(component),['empty','filled','error']),('standalone',standalone,['empty','filled','error','blocked','external']),
        ('butler',butler,['empty','filled','error']),('packages',package_editor,['empty','filled','error']),('history',history,['empty','filled','shared','error']),
        ('two-mounts',two_mounts,['filled']),('context',context_editor,['filled']),
        ('share',share_preview,['filled','denied']),('model-context',model_preview,['filled','denied'])]:
        cfg=config(builder(),surface)
        save(f'{surface}-{theme}.cellconfiguration.json',cfg)
        for kind in kinds:
            state=dict(chat=mount_value(component,helper_state(kind)),
                       chatB=mount_value(component,helper_state('empty','demo-session-02','Mitt eget idéutkast')),
                       package=dict(title='Min prosjektassistent',titleLabel='Min prosjektassistent',
                                    versionLabel='Privat · mitt utkast · basert på Idéutvikling v3',
                                    skillsLabel='haven-work-intake · formålsdrevet utvikling',
                                    contextLabel='Prosjektets README · valgt oppgave · mine notater',notices=[],
                                    purposes=[dict(id='demo-purpose-01',title='Sammenhengende navigasjon'),dict(id='demo-purpose-02',title='Fra idé til utførbar oppgave')],purpose='demo-purpose-01',
                                    instructions='Hjelp meg å utforske ideer for CellScaffold.\nStill ett avklarende spørsmål om gangen.\nKnytt forslag til formål og konkrete akseptkriterier.\nOpprett arbeidsordre først når omfanget er tydelig.'),
                       history=dict(scopes=[dict(id='private',title='Min private historikk'),dict(id='project',title='Prosjektets delte historikk')],
                                    scope='private',scopeLabel='Privat historikk · bare du ser samtaletekst og personlige notater',
                                    modes=[dict(id='text',title='Tekst'),dict(id='purpose',title='Formål')],mode='text',query='tilbakeknapp',notices=[],
                                    results=[dict(id='demo-event-01',title='Idé om en bedre tilbakeknapp',
                                                  provenance='10. oktober, 10:34 · Hjelpechat · privat',
                                                  excerpt='«Jeg vil komme tilbake til samme prosjekt når jeg lukker porteføljen.»',
                                                  relations='Knyttet til: DEMO-014 · CellScaffold · sammenhengende navigasjon'),
                                             dict(id='demo-event-02',title='Prosjektet fikk en ny oppgave',
                                                  provenance='10. oktober, 10:39 · Work Item · delt med prosjektet',
                                                  excerpt='DEMO-014 ble opprettet med mål og akseptkriterier. Privat samtale er ikke vedlagt.',
                                                  relations='Kilde: Work Item DEMO-014')]))
            state['context']=dict(skills=[dict(id='demo-skill-01',title='haven-work-intake',detail='Valgt · idéfangst og arbeidsordre',label='Fjern'),
                                          dict(id='demo-skill-02',title='Formålsdrevet utvikling',detail='Tilgjengelig · formål og mål',label='Legg til')],
                                  sources=[dict(id='demo-source-01',title='Oppgave DEMO-014',detail='Valgt · prosjektdata',label='Fjern'),
                                           dict(id='demo-source-02',title='Offentlig README',detail='Valgt · to avgrensede utdrag',label='Fjern'),
                                           dict(id='demo-source-03',title='Mine private notater',detail='Ikke valgt · kun synlig for meg',label='Legg til')])
            state['review']=dict(audiences=[dict(id='demo-project',title='CellScaffold · prosjektmedlemmer'),dict(id='private',title='Bare meg')],
                                 audience='demo-project',notices=[],actions=[])
            if surface=='share' and kind=='filled':
                state['review']['actions']=[dict(label='Del versjon 3 med prosjektet',keypath='helper.sharePackageVersion',
                                                payload={'sharePreviewID':'demo-share-01','expectedRevision':3})]
            if surface=='model-context' and kind=='filled':
                state['review']['actions']=[dict(label='Bruk dette datagrunnlaget',keypath='helper.confirmModelContext',
                                                payload={'contextPreviewID':'demo-context-01','expectedRevision':2})]
            if kind=='denied':
                state['review']['notices']=[dict(title='Tilgang mangler',body='Gjeldende avtale tillater ikke denne delingen.' if surface=='share' else 'Denne modellruten er ikke tillatt for valgt prosjekt. Velg en annen modell eller avgrens konteksten.')]
            if surface=='history':
                if kind=='shared':
                    state['history'].update(scope='project',scopeLabel='CellScaffold · prosjektets delte hendelser · ingen privat samtaletekst')
                    state['history']['results']=state['history']['results'][1:]
                else:
                    state['history']['results']=state['history']['results'][:1]
            if surface=='packages' and kind=='empty':
                state['package'].update(title='',titleLabel='Ny perspektivpakke',versionLabel='Privat · ikke lagret',instructions='',
                                        skillsLabel='Ingen skills valgt',contextLabel='Ingen kontekst valgt')
            if surface=='packages' and kind=='error':
                state['package']['notices']=[dict(title='En nyere versjon finnes',body='Utkastet ditt er bevart. Sammenlign endringene før du lagrer en ny versjon.')]
            if surface=='history' and kind in ['empty','error']:
                state['history']['results']=[]
                state['history']['notices']=[dict(title='Ingen treff' if kind=='empty' else 'Historikken er ikke tilgjengelig',
                    body='Prøv et annet søkeord eller velg formål.' if kind=='empty' else 'Søket kunne ikke fullføres. Prøv igjen når forbindelsen er tilbake.')]
            if surface=='two-mounts': state['chat']['item']['draft']='Rett tilbakeknappen'
            name=f'{surface}-{kind}-{theme}'
            save(name+'.state.json',state)
            shots.append(dict(name=name,configuration=f'{surface}-{theme}.cellconfiguration.json',state=name+'.state.json',
                              theme=theme,width=1440 if surface=='workbench' else 1180,height=900))
    for kind in ['empty','filled','error']:
        shots.append(dict(name=f'standalone-{kind}-{theme}-narrow',configuration=f'standalone-{theme}.cellconfiguration.json',
                          state=f'standalone-{kind}-{theme}.state.json',theme=theme,width=390,height=844))
save('shots.json',shots)
print(f'{len(shots)} rendering cases; {len(list(OUT.glob("*.json")))} JSON files')
