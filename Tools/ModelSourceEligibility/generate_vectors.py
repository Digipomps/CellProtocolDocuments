import json,sys
P='purpose://candidate.model-source.'
NOW=1794900000
def src(cls,**k):
    d={"id":cls,"servingClass":cls,"servesWhom":"agreement","availableWhenOwnerOffline":"unknown","declaredAvailable":False,"health":{"status":"unknown"},"region":"unknown"}
    d.update(k); return d
def ok(age=60,p50=3000): return {"status":"ok","measuredAtEpoch":NOW-age,"p50Ms":p50}
def laptop(**k):
    b=dict(id="agent.local-model.owner-laptop",availableWhenOwnerOffline="no",declaredAvailable=True,health=ok(120,3800)); b.update(k); return src("personal_device",**b)
def hosted(**k):
    b=dict(id="dimy.mistral-small",availableWhenOwnerOffline="yes",region="EU",pricePerMTokInput="1.60",pricePerMTokOutput="6.20",offeredByDiMy=True,health=ok()); b.update(k); return src("hosted_provider",**b)
def hostllm(**k):
    b=dict(id="local.qwen3.8b",availableWhenOwnerOffline="yes",hostFacts={"gpu":"none","vcpu":4,"freeRamGiB":8,"sharedWith":["staging","prod"],"measuredAtEpoch":1794816000}); b.update(k); return src("operator_host",**b)
rules=src("rules",id="chat.local-rules",availableWhenOwnerOffline="yes")
def ctx(**k):
    d={"nowEpoch":NOW,"requesterIsOwner":False,"requesterHasAccess":True,"explicitChoice":False,"fallbackAvailable":True}; d.update(k); return d
D,U,S=P+"develop-and-test",P+"personal-daily-use",P+"service-for-others"
cases=[]
def c(name,purpose,source,context,eligible,unmet,effective=None,profile=None,rejected=None):
    e={"eligible":eligible,"unmet":unmet,"effectivePurposeRef":effective or purpose,"rejectedLoosenings":rejected or []}
    d={"name":name,"purposeRef":purpose,"source":source,"context":context,"expect":e}
    if profile is not None: d["profile"]=profile
    cases.append(d)
own=dict(requesterIsOwner=True)
c("dev: eier, laptop erklært",D,laptop(),ctx(**own),True,[])
c("dev: eier, laptop ikke erklært",D,laptop(declaredAvailable=False),ctx(**own),False,["declared_available"])
c("dev: eier, laptop helse feilet",D,laptop(health={"status":"failed","measuredAtEpoch":NOW-30}),ctx(**own),False,["health_measured_ok"])
c("dev: hostet uten måling er lov",D,hosted(health={"status":"unknown"}),ctx(**own),True,[])
c("dev: Agreement-holder velger laptopen selv",D,laptop(),ctx(explicitChoice=True),True,[])
c("dev: Agreement-holder, laptop ikke valgt selv",D,laptop(),ctx(),False,["owner_or_explicit_choice"])
c("dev: fremmed uten Agreement, selv om valgt",D,laptop(),ctx(requesterHasAccess=False,explicitChoice=True),False,["access_via_agreement"])
c("daglig: eier, laptop med reserve",U,laptop(),ctx(**own),True,[])
c("daglig: eier, laptop uten reserve",U,laptop(),ctx(fallbackAvailable=False,**own),False,["fallback_present"])
c("daglig: hostet",U,hosted(),ctx(**own),True,[])
c("tjeneste: laptop aldri, selv for eier",S,laptop(),ctx(**own),False,["serving_class_allowed","available_when_owner_offline"])
c("tjeneste: laptop aldri, selv valgt selv",S,laptop(),ctx(explicitChoice=True),False,["serving_class_allowed","available_when_owner_offline"])
c("tjeneste: hostet målt ok",S,hosted(),ctx(),True,[])
c("tjeneste: hostet uten måling",S,hosted(health={"status":"unknown"}),ctx(),False,["health_measured_ok","response_time_within_limit"])
c("tjeneste: hostet, måling for gammel",S,hosted(health=ok(601)),ctx(),False,["health_measured_ok"])
c("tjeneste: hostet, måling akkurat på grensen",S,hosted(health=ok(600)),ctx(),True,[])
c("tjeneste: hostet for treg i chat",S,hosted(health=ok(60,45000)),ctx(),False,["response_time_within_limit"])
c("tjeneste: samme svartid holder i Kallimachos",S,hosted(health=ok(60,45000)),ctx(surface="kallimachos"),True,[])
c("tjeneste: vertsmodell uten måling (staging 16.11)",S,hostllm(),ctx(surface="kallimachos"),False,["health_measured_ok","response_time_within_limit"])
c("tjeneste: vertsmodell målt for treg på CPU",S,hostllm(health=ok(60,240000)),ctx(surface="kallimachos"),False,["response_time_within_limit"])
c("tjeneste: vertsmodell målt innenfor",S,hostllm(health=ok(60,20000)),ctx(surface="kallimachos"),True,[])
c("tjeneste: vertsmodell som ikke melder frakoblet-evne",S,hostllm(availableWhenOwnerOffline="unknown",health=ok()),ctx(),False,["available_when_owner_offline"])
c("tjeneste: regler alltid",S,rules,ctx(requesterHasAccess=False),True,[])
c("tjeneste: ukjent kildeklasse",S,src("unknown",id="custom.x",availableWhenOwnerOffline="yes",health=ok()),ctx(),False,["serving_class_allowed"])
c("tjeneste: hostet uten Agreement",S,hosted(),ctx(requesterHasAccess=False),False,["access_via_agreement"])
c("daglig: enheten spørreren sitter ved, uten reserve",U,src("requester_device",id="chat.apple-intelligence",servesWhom="owner_only",availableWhenOwnerOffline="no"),ctx(fallbackAvailable=False,**own),True,[])
c("tjeneste: enheten spørreren sitter ved kan ikke bære en tjeneste",S,src("requester_device",id="chat.apple-intelligence",servesWhom="owner_only",availableWhenOwnerOffline="no",health=ok()),ctx(**own),False,["serving_class_allowed","available_when_owner_offline"])
c("ukjent formål gir strengeste",'purpose://prompt.unknown',laptop(),ctx(**own),False,["serving_class_allowed","available_when_owner_offline"],effective=S)
c("tomt formål gir strengeste","",hosted(),ctx(),True,[],effective=S)
c("profil strammer: bare EU",U,hosted(region="US"),ctx(**own),False,["region_allowed"],profile={"allowedRegions":["EU"]})
c("profil strammer: ingen laptop i daglig bruk",U,laptop(),ctx(**own),False,["serving_class_allowed"],profile={"allowedServingClasses":["rules","hosted_provider","operator_host"]})
c("profil strammer: krever måling også i utvikling",D,hosted(health={"status":"unknown"}),ctx(**own),False,["health_measured_ok"],profile={"requireMeasuredHealth":True,"maxHealthAgeSeconds":300})
c("profil prøver å løsne: laptop i tjeneste",S,laptop(),ctx(**own),False,["serving_class_allowed","available_when_owner_offline"],profile={"allowedServingClasses":["rules","requester_device","personal_device","operator_host","hosted_provider"],"requireAvailableWhenOwnerOffline":False},rejected=["allowedServingClasses","requireAvailableWhenOwnerOffline"])
c("profil prøver å løsne: høyere svartid og eldre måling",S,hosted(health=ok(900,45000)),ctx(),False,["health_measured_ok","response_time_within_limit"],profile={"maxHealthAgeSeconds":3600,"maxP50MsBySurface":{"default":120000}},rejected=["maxHealthAgeSeconds","maxP50MsBySurface"])
c("profil strammer svartid",S,hosted(health=ok(60,20000)),ctx(),False,["response_time_within_limit"],profile={"maxP50MsBySurface":{"default":10000}})
out=sys.argv[1]
with open(out,'w') as f:
    json.dump({"schema":"haven.model-source-eligibility.vectors.v1","contract":"Book/model_source_eligibility_contract_v1.json","cases":cases},f,ensure_ascii=False,indent=2); f.write('\n')
print(len(cases))
