**Tre: startverdier fra mockupens CSS**

Dette er starttabellen for iterasjon, ikke målte rendererresultater. Alle CSS-kilder er i `HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html`; linjenummer følger selektoren. CSS-variablene løses fra linje7–11: surface=#ffffff, bg=#f3f7fb, text=#17212b, muted=#556273, primary=#0f4c81, border=#d5e0eb, branch-a=#0f8a61, branch-b=#7a4fbf, accent=#ef7c2d, radius=10. Ingen stilklasse fra mockupen brukes som skjult rendererimplementering.

| selektor (CSS-kildelinje) | CSS-verdi | modifikatorfelt | startverdi |
|---|---|---|---|
| body (:15) | color var(--text); font14px/1.45 | Text/Button.foregroundColor, fontSize, fontWeight | #17212b,14,"400"; vekt400 fra normal body-font |
| .stage (:29), body (:15) | background var(--bg); gap14 | rot.background; VStack.spacing | #f3f7fb;14 |
| .panel.rail (:29–31) | kolonne288; height=1250−52−2×14 | width,height | 288,1170 for isolert webreferanse; ikke adaptivt |
| .panel (:31) | surface; border1 solid border; radius10 | background,borderWidth,borderColor,cornerRadius | #ffffff,1,#d5e0eb,10 |
| .panel > header (:32) | padding11px13px | padding | 11 på alle sider; horisontal13 mangler, +2 per side senere |
| .panel > header (:32) | gap8 | HStack.spacing | 8 |
| .panel > header (:32), .tree-foot (:51) | bunn-/toppkant1 solid border | tom VStack.height,background | 1,#d5e0eb som egne delere; ikke allekantersborder |
| .panel h2 (:33) | font-size13; weight600; letter-spacing.2 | fontSize,fontWeight; letterSpacing finnes ikke | 13,"600"; bokstavavstand utelatt |
| .panel header .sub (:34) | font-size12; muted | fontSize,foregroundColor,fontWeight | 12,#556273,"400" |
| .tree (:37) | padding6px6px10px | List.padding | 6; bunn10 mangler (+4) |
| .node (:38) | gap7; padding5px8px; radius7 | HStack.spacing,padding,cornerRadius | indre gap7; ytre gap0; padding5; radius7 |
| .node og .d1/.d2 (:38,:49) | venstre8/16/32, høyre8 | faste tomme VStack.width | venstre3/11/27 (=8/16/32−5), høyre3 (=8−5); ytre padding5. Avledede verdier, ikke nye designtokens. |
| .node normal / .panel (:31,:38) | transparent node over hvit surface | background | #ffffff som eksplisitt ekvivalent bakgrunn i kandidaten |
| .node.sel (:46) | background#e8f1f9; weight600 | background; label/arrow/count/kind.fontWeight | #e8f1f9;"600". Tekstvekten gjentas eksplisitt fordi app ikke arver containerfont på samme måte. |
| .node.inscope (:48) | background#f3f8fc | background | #f3f8fc |
| .node .tw (:40) | width14; size10; muted | width,fontSize,foregroundColor | 14,10,#556273; blank bladplass har samme bredde |
| button (:16), .node .tw / .label (:40,:44) | border0; ingen ekstra nodeknapp-padding/radius; inherit font | Button.borderWidth,padding,cornerRadius,background | 0,0,0; radens #ffffff/#e8f1f9/#f3f8fc som bakgrunn. Dette nøytraliserer ikke web-CSS-border i dagens renderer. |
| .node .dot (:41) | width7;height7;border-radius50%; border-farge | width,height,cornerRadius,background | 7,7,3.5 (=halv7),#d5e0eb |
| .node.branch .dot (:42), :root (:11) | branch-a | background | #0f8a61 i lokal branchA-variant |
| .node.branch-b .dot (:43), :root (:11) | branch-b | background | #7a4fbf i lokal branchB-variant |
| feil .branch-b .dot (:211), :root (:9) | accent | background | #ef7c2d i lokal declined-variant |
| .node .label (:44), body (:15) | flex1/min-width0/ellipsis/nowrap; font14 | maxWidthInfinity,lineLimit,multilineTextAlignment,fontSize,foregroundColor | true,1,"leading",14,#17212b. Dette er ikke ekvivalent flex1/min-width0 på web. |
| .node .kind (:50) | font11; muted; border1; radius4; padding0px4px; line-height15px | fontSize,foregroundColor,borderWidth,borderColor,cornerRadius,padding,height | 11,#556273,1,#d5e0eb,4,0,15. Horisontal4 utelatt; height15 er ikke lineHeight15. |
| .node .count (:45) | font12; muted; tabular-nums | fontSize,foregroundColor | 12,#556273; numericVariant finnes ikke |
| .tree-foot (:51) | padding9px12px; gap8; font12; muted | padding,HStack.spacing,fontSize,foregroundColor | 9,8,12,#556273; horisontal12 mangler (+3) |
| .chip (:69) | font11; radius20; padding1px8px; border1; muted | fontSize,cornerRadius,padding,borderWidth,borderColor,foregroundColor | 11,20,1,1,#d5e0eb,#556273; horisontal8 mangler (+7) |
| .topbar (:19) | height52; surface | HStack.height,background | 52,#ffffff; bare delens kontroller, ikke hele topplinjen |
| .topbar .right (:24) | gap10 | HStack.spacing | 10 i kontrollgruppen |
| .seg (:54) | border1 solid border; radius7; inline-flex | borderWidth,borderColor,cornerRadius; HStack.spacing | 1,#d5e0eb,7;0 mellom segmentene |
| .seg button (:55) | padding3px9px; font12; muted | padding,fontSize,fontWeight,foregroundColor,background | 3,12,"400",#556273,#ffffff. Horisontal9 mangler (+6). |
| .seg button.on (:56) | primary; white | background,foregroundColor | #0f4c81,#ffffff |
| .seg button (:54–56), button (:16) | enkeltknapp uten egen border/radius | borderWidth,cornerRadius | 0,0; gruppen har ytterkant. Webborder0-overstyring og gruppeklipp mangler. |
| .treebtn (:186) | border1 solid border; radius7; padding3px9px; font12; muted | borderWidth,borderColor,cornerRadius,padding,fontSize,foregroundColor,background | 1,#d5e0eb,7,3,12,#556273,#ffffff; horisontal9 mangler; ☰-ikon ikke tatt med |
| app .topbar / .seg button (:166,:168) | height46; padding3px7px; font11.5 | ingen separat appvariant i kandidaten | beholder52 / padding3 / font12. Endring krever avklart layoutkontekst, ikke viewport-magikk. |

`hAlignment:"leading"` og `maxWidthInfinity:true` er layoutintensjon (startjusterte panel/rader og fylle tilgjengelig bredde), utledet fra flexoppsettet i CSS:31/38/44; de er ikke direkte oversettelser av en CSS-egenskap. `visibility` er itemdata for å velge en konstant stilvariant, ikke en modifikatorverdi hentet fra CSS. Bare d0/d1/d2 er representert; d3=48 i CSS:49 er utenfor referansebildene og kandidaten.

Verdier som krever nye felt eller rendereravklaring før pixeliterasjon:

| selektor | manglende uttrykk / presis målverdi | forslag, ikke i JSON |
|---|---|---|
| body og all tekst (:15) | fontfamilie Avenir Next → Segoe UI → system-ui → sans-serif; line-height1.45 | fontFamily, lineHeight. Referanser er rendret på en annen Chromium-vert; hvilken fallbackfont som faktisk ble brukt er ukjent. |
| .panel h2 (:33) | letter-spacing0.2px | letterSpacing:0.2 |
| .node:hover (:39) | background#f8fbfe | hoverBackground; renderer må fjerne Button-transform ved radbetjening |
| .node.sel::before (:47) | left−6,top4,bottom4,width3,radius2,primary | leadingMarker uten layoutbidrag; helt utelatt i kandidaten |
| alle asymmetriske insets | CSS-kantene over, ikke én scalar | paddingInsets; eventuelt paddingLeadingKeypath for én flat mal |
| .node .count (:45) | tabular-nums | numericVariant:tabular |
| .node .label (:44) | flex-grow1,min-width0,ellipse i én linje | flexGrow:1,minWidth:0; felles tekstlayout |
| .seg / .panel (:31,:54) | overflow:hidden ved avrundingen | renderer må klippe innhold til rammen; cornerRadius alene er ulikt web/app |

Den numeriske CSS-vekten "600" er beholdt som startverdi og viser et reelt paritetsgap: web setter string direkte; app støtter navn som "semibold", mens "600" faller tilbake til regular. Å bytte til "semibold" bare i JSON retter ikke begge renderere, fordi det ikke er en CSS font-weight-verdi. Kilder: `CellScaffold/Public/js/skeleton-runtime.js:4140`; `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:33`. Scalarpadding/border0-begrensningen står i `CellScaffold/Public/js/skeleton-runtime.js:4112`, `:4167`; appens modifikatorrekkefølge i `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:702`.

Iterer først når nødvendige data og rendererfelter finnes: mål radhøyde, x-posisjoner (pil/prikk/label/merke/tall), header/fot, baseline og markør på samme viewport. Endre én verdi om gangen og behold skjermbildene. Ikke kompenser for manglende font eller ekstra List-padding med vilkårlige nye designtall. Sammenligningskart og scenarioforbehold står i `handoff/SKJELETT_GAP_tre.md`.
