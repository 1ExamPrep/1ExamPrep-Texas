/* Exam advisor ("Max") inside the site search. Loaded by search.js only when "aiFinderUrl" is set in site-config.json.

   Built so anyone can use it without typing: one easy question at a time with big buttons (trade, license, what
   they want), then the best package with Buy now. Those steps run right here from shared/kb/products.json, so they
   are instant and cost nothing. A typed question goes to the AI on the Cloudflare Worker (1exam-texas), which
   answers from shared/kb/texas.json. Buy now uses the same tagged checkout links as the rest of the site. */
(function(){
  "use strict";
  var S=window.SRCH, SITE=window.SITE||{}; if(!S||!SITE.aiFinder) return;
  var ENDPOINT=SITE.aiFinder.replace(/\/+$/,"")+(/\/chat$/.test(SITE.aiFinder)?"":"/chat");
  var STORE=(SITE.storeUrl||"https://1examprep.com").replace(/\/+$/,""), KEY="max_tx_v1", NAME="Max";
  var PHONE=SITE.phone||((document.querySelector('a[href^="tel:"]')||{}).textContent||"").trim();
  var DATA=null;
  function hello(){var h=new Date().getHours();return h<5?"Hi":h<12?"Good morning":h<18?"Good afternoon":"Good evening";}
  function greeting(){return hello()+"! I'm "+NAME+". I'll help you find the right prep for your Texas license, and I understand full sentences, so ask me anything in your own words.\n\nOr just tap your answers below.";}

  /* ---- the guided questions ---- */
  var TRADES=[
    {v:"electrical",e:"⚡",t:"Electrician",s:"Journeyman, master, wireman, sign, lineman and more"},
    {v:"plumbing",e:"🔧",t:"Plumber",s:"Tradesman, journeyman, master or plumbing inspector"},
    {v:"acr",e:"❄️",t:"A/C and refrigeration",s:"Class A or B contractor, or certified technician"},
    {v:"other",e:"🏗️",t:"Something else",s:"City exams, code enforcement, ICC, NASCLA or business setup"}
  ];
  var OTHER=["local","business","national","codes"];
  var WANTS=[
    {v:"everything",e:"⭐",t:"Everything",s:"Best chance to pass, all in one order"},
    {v:"books",e:"📘",t:"Books and code books",s:"Study guides and the references"},
    {v:"online",e:"💻",t:"Online course",s:"Practice tests on your phone or laptop"},
    {v:"cheapest",e:"💵",t:"Cheapest way to start",s:"The lowest price option"},
    {v:"help",e:"🙋",t:"Help me choose",s:"Show me the best one"}
  ];
  var LEVEL_HELP={electrical:"No problem. Most people start with Journeyman Electrician after 8,000 hours on the job, or Residential Wireman after 4,000. Master comes after 2 years as a journeyman.",
                  plumbing:"No problem. Tradesman Plumber-Limited needs 4,000 hours, Journeyman 8,000 hours and a 48-hour course, and Master comes after 2 years as a journeyman.",
                  acr:"No problem. Class B covers systems up to 25 tons cooling, Class A has no limit. Both need 48 months of experience. The certified technician exam needs 24 months."};

  function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
  function money(v){v=Number(v);return "$"+(v%1?v.toFixed(2):String(v)).replace(/\B(?=(\d{3})+(?!\d))/g,",");}
  function cartUrl(vid){return STORE+"/cart/"+vid+":1"+(SITE.cartTag||"");}
  function load(){try{return JSON.parse(sessionStorage.getItem(KEY));}catch(e){return null;}}
  function save(){try{sessionStorage.setItem(KEY,JSON.stringify(st));}catch(e){}}
  function fresh(){return {messages:[],slots:{},view:[],greet:greeting()};}
  var st=load()||fresh(), busy=false;
  var reduceMotion=!!(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  function ensureData(cb){
    if(DATA){cb();return;}
    if(ensureData.cbs){ensureData.cbs.push(cb);return;}
    ensureData.cbs=[cb];
    fetch(S.BASE+"shared/kb/products.json").then(function(r){return r.json();}).then(function(d){DATA=d;}).catch(function(){DATA={items:[],licenses:[],want:{}};})
      .then(function(){var c=ensureData.cbs;ensureData.cbs=null;c.forEach(function(f){f();});});
  }
  function lic(slug){return (DATA.licenses||[]).filter(function(l){return l.s===slug;})[0];}
  function item(id){return (DATA.items||[]).filter(function(p){return p.id===String(id);})[0];}

  var ov=S.ov, box=ov.querySelector(".srch-box"), form=box.querySelector(".srch-form"), res=box.querySelector(".srch-res"), hint=box.querySelector(".srch-hint");
  var css=document.createElement("link"); css.rel="stylesheet"; css.href=S.BASE+"shared/max.css"; document.head.appendChild(css);
  var AVATAR='<span class="ai-av" aria-hidden="true">'+NAME.charAt(0)+'</span>';
  var panel=document.createElement("div"); panel.className="ai"; panel.hidden=true;
  panel.innerHTML='<div class="ai-head">'+AVATAR+'<div class="ai-who"><b>'+NAME+' <span class="ai-ailabel">AI</span></b><small><i class="ai-on-dot"></i><span class="ai-status">Texas exam helper · online</span></small></div><span class="ai-sp"></span><button type="button" class="ai-link" data-ai-reset>Start over</button><button type="button" class="ai-link" data-ai-back>Search instead</button><button type="button" class="srch-x" data-sclose aria-label="Close">×</button></div>'+
    '<div class="ai-log" aria-live="polite"></div><div class="ai-chips"></div>'+
    '<form class="ai-form" autocomplete="off"><input class="ai-in" type="text" maxlength="400" placeholder="Or type a question for '+NAME+'…" aria-label="Type a question"><button class="ai-send" type="submit" aria-label="Send"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M3 11.5 21 3l-8.5 18-2.2-7.3L3 11.5Z" fill="currentColor"/></svg></button></form>'+
    '<p class="ai-foot">'+NAME+' is an AI helper and only shows products we really sell.'+(PHONE?' Want a person? Call <a href="tel:'+esc(PHONE.replace(/[^0-9+]/g,""))+'">'+esc(PHONE)+'</a>.':'')+'</p>';
  box.appendChild(panel);
  var log=panel.querySelector(".ai-log"), chips=panel.querySelector(".ai-chips"), aForm=panel.querySelector(".ai-form"), input=panel.querySelector(".ai-in"), sendBtn=panel.querySelector(".ai-send"), status=panel.querySelector(".ai-status");

  function parts(text){return String(text||"").split(/\n\s*\n/).map(function(x){return x.trim();}).filter(Boolean).slice(0,3);}
  function scroll(){log.scrollTop=log.scrollHeight;}
  function row(role){var r=document.createElement("div"); r.className="ai-line "+role; if(role==="bot") r.innerHTML=AVATAR; log.appendChild(r); return r;}
  function bubble(role,text,isNew){
    var r=row(role), d=document.createElement("div"); d.className="ai-msg "+role+(isNew&&!reduceMotion?" pop":""); d.textContent=text; r.appendChild(d);
    var prev=r.previousElementSibling; if(role==="bot"&&prev&&prev.classList.contains("bot")) prev.classList.add("cont");
    scroll(); return d;
  }

  /* ---- products ---- */
  function cards(products){
    if(!products||!products.length) return;
    var html=products.map(function(x,i){
      var p=item(x.id); if(!p) return "";
      var l=lic(p.c)||{n:p.cn};
      return '<article class="ai-card'+(i===0?" top":"")+'" data-id="'+esc(p.id)+'"><img src="'+esc(p.i)+'" alt="'+esc(p.t)+'" loading="lazy" width="88" height="88">'+
        '<div>'+(i===0?'<span class="ai-badge">⭐ Best for you</span>':'<span class="ai-badge alt">Also good</span>')+'<h3>'+esc(p.tn)+'</h3><small>'+esc(l.n+(p.y&&p.c.indexOf("electric")>-1?" · "+p.y+" code":"")+(p.rg==="Texas"?"":" · any state"))+'</small>'+
        (x.why?'<p class="ai-why">'+esc(x.why)+'</p>':"")+
        '<div class="ai-row"><span class="ai-price">'+money(p.p)+'</span><a class="btn btn-buy ai-btn" href="'+esc(cartUrl(p.v))+'" rel="noopener" data-buy="'+esc(p.id)+'">Buy now</a><a class="ai-more" href="'+esc(S.BASE+p.u)+'">See what’s inside</a></div></div></article>';
    }).join("");
    if(!html) return;
    var w=document.createElement("div"); w.className="ai-cards"+(reduceMotion?"":" pop"); w.innerHTML=html; log.appendChild(w); scroll();
  }
  var WHY={everything:"Everything for this exam in one order.",books:"The books and references you study from.",online:"Timed practice you can do anywhere.",cheapest:"The lowest price way to start.",
           "the-1-package":"Exam prep, books, the license application and business setup in one.","ultimate-rental":"Highlighted rental books, the online course and live training.",
           "ultimate-combo":"The full study set plus the online test kit.","highlighted-tabbed":"The books already highlighted, ready for the exam room."};
  /* best package for the answers given, plus one other good option */
  function localPicks(sl){
    var all=(DATA.items||[]).filter(function(p){return p.c===sl.license&&p.a;});
    if(!all.length) return [];
    var C=all.filter(function(p){return p.cur&&p.rg==="Texas";}); if(!C.length) C=all.filter(function(p){return p.cur;}); if(!C.length) C=all;
    var W=DATA.want||{};
    function inWant(k){var t=W[k]||[];return C.filter(function(p){return t.indexOf(p.ty)>-1;});}
    function best(list){return list.slice().sort(function(a,b){return b.r-a.r||a.p-b.p;})[0];}
    function cheap(list){return list.slice().sort(function(a,b){return a.p-b.p;})[0];}
    var top, alt, w=sl.want||"help";
    if(w==="cheapest"){top=cheap(C);alt=best(C);}
    else if(w==="books"||w==="online"||w==="everything"){var L=inWant(w);top=w==="online"?cheap(L):best(L);alt=w==="everything"?cheap(C):best(C);top=top||best(C);}
    else {var B=DATA.best||[];for(var k=0;k<B.length&&!top;k++){top=best(C.filter(function(p){return p.ty===B[k];}));} top=top||best(C); alt=cheap(C);}
    return [top,alt].filter(function(p,i,a){return p&&a.indexOf(p)===i;}).map(function(p,i){return {id:p.id,why:WHY[p.ty]||(i===0?WHY[w]:"")||""};});
  }

  /* ---- big tap buttons ---- */
  function bigButtons(list,kind){
    return '<div class="ai-big" data-kind="'+kind+'">'+list.map(function(o){
      return '<button type="button" class="ai-bigbtn" data-pick="'+esc(o.v)+'" data-label="'+esc(o.t)+'"><span class="ai-emo" aria-hidden="true">'+o.e+'</span><span><b>'+esc(o.t)+'</b><small>'+esc(o.s)+'</small></span></button>';
    }).join("")+'</div>';
  }
  function licensePicker(trade){
    var gs=trade==="other"?OTHER:[trade];
    var L=(DATA.licenses||[]).filter(function(l){return gs.indexOf(l.g)>-1;});
    return '<div class="ai-big ai-lics" data-kind="license">'+L.map(function(l){return '<button type="button" class="ai-lic" data-pick="'+esc(l.s)+'" data-label="'+esc(l.n)+'">'+esc(l.n)+'<small>from '+money(l.lo)+'</small></button>';}).join("")+
      (trade!=="other"?'<button type="button" class="ai-lic" data-pick="unsure" data-label="I\'m not sure">🤔 I’m not sure</button>':"")+'</div>';
  }
  function pickerFor(step){
    if(step==="trade") return bigButtons(TRADES,"trade");
    if(step==="license") return licensePicker(st.slots.trade||"electrical");
    if(step==="want") return bigButtons(WANTS,"want");
    if(step==="done"){var l=lic(st.slots.license)||{n:"this license",s:""};return '<div class="ai-after"><a class="ai-all" href="'+esc(S.BASE+l.s+"/")+'">See every '+esc(l.n)+' option</a><button type="button" class="ai-again" data-ai-reset>Start over</button></div>';}
    return "";
  }
  function showPicker(step){
    log.querySelectorAll(".ai-pickwrap").forEach(function(n){n.remove();});
    var html=pickerFor(step); if(!html) return;
    var w=document.createElement("div"); w.className="ai-pickwrap"+(reduceMotion?"":" pop"); w.innerHTML=html; log.appendChild(w); scroll();
  }
  function needStep(sl){ if(!sl.license&&!sl.trade) return "trade"; if(!sl.license) return "license"; if(!sl.want) return "want"; return "done"; }
  var QUESTION={trade:"What kind of license are you going for?",license:"Which license is it?",want:"What do you want to get?"};

  /* ---- conversation ---- */
  var greetRun=null;
  function render(animate){
    log.innerHTML=""; setChips([]);
    if(animate&&!st.view.length){ var g=greetRun={stop:false}; deliver(st.greet||greeting(),[],[],g).then(function(){ if(greetRun===g){greetRun=null; ask(needStep(st.slots));} }); return; }
    parts(st.greet||greeting()).forEach(function(t){bubble("bot",t);});
    st.view.forEach(function(v){ if(v.type==="user") bubble("user",v.text); else { parts(v.text).forEach(function(t){bubble("bot",t);}); cards(v.products); } });
    var last=st.view[st.view.length-1];
    if(last&&last.type==="bot"){ if(last.step) showPicker(last.step); setChips(last.step&&last.step!=="done"?[]:(last.suggestions||[])); }
    else if(!st.view.length) ask(needStep(st.slots));
  }
  function ask(step,lead){
    if(step==="done") return showResults(lead);
    var text=(lead?lead+"\n\n":"")+(QUESTION[step]||"");
    st.view.push({type:"bot",text:text,step:step}); st.messages.push({role:"assistant",content:text}); save();
    return deliver(text,[],[]).then(function(){showPicker(step);});
  }
  function showResults(lead){
    var picks=localPicks(st.slots), l=lic(st.slots.license)||{n:""};
    var text=picks.length?(lead?lead+"\n\n":"")+"Here's the best one for the "+l.n+" exam. Tap Buy now when you're ready.":"Hmm, I couldn't find packages for that one. Try another license, or call us"+(PHONE?" at "+PHONE:"")+".";
    var sugg=["How are they different?","Is the exam open book?"];
    st.view.push({type:"bot",text:text,products:picks,step:picks.length?"done":"trade",suggestions:sugg});
    st.messages.push({role:"assistant",content:text+(picks.length?" [Shown: "+picks.map(function(x){var p=item(x.id);return p.cn+" "+p.tn+" "+money(p.p);}).join("; ")+"]":"")});
    save(); track("ai_advisor_recommend",{products:picks.map(function(p){return p.id;}).join(","),mode:"guided"});
    return deliver(text,picks,sugg).then(function(){showPicker(picks.length?"done":"trade");});
  }
  function choose(kind,value,label){
    if(busy) return;
    if(greetRun){greetRun.stop=true;greetRun=null;}
    log.querySelectorAll(".ai-pickwrap").forEach(function(n){n.remove();}); setChips([]);
    st.view.push({type:"user",text:label}); st.messages.push({role:"user",content:label}); bubble("user",label,true);
    track("ai_advisor_tap",{step:kind,value:value});
    var lead="";
    if(kind==="trade"){ st.slots.trade=value; delete st.slots.license; lead={electrical:"Electrician, great.",plumbing:"Plumbing, nice.",acr:"A/C and refrigeration, got it.",other:"Sure."}[value]||""; }
    if(kind==="license"){
      if(value==="unsure"){ save(); return ask("license",LEVEL_HELP[st.slots.trade]||"No problem, here are the options."); }
      st.slots.license=value; var l=lic(value); if(l) st.slots.trade=OTHER.indexOf(l.g)>-1?"other":l.g; lead=(l?l.n:"That one")+", good choice.";
    }
    if(kind==="want"){ st.slots.want=value; lead=value==="help"?"Sure, here's what I'd get.":"Good pick."; }
    save();
    return ask(needStep(st.slots),lead);
  }

  function setChips(list){ chips.innerHTML=(list||[]).map(function(s){return '<button type="button" class="ai-chip">'+esc(s)+'</button>';}).join(""); }
  function typing(){
    var r=row("bot"); r.classList.add("typing");
    var d=document.createElement("div"); d.className="ai-msg bot"; d.innerHTML='<span class="ai-dots"><i></i><i></i><i></i></span>'; r.appendChild(d);
    var prev=r.previousElementSibling; if(prev&&prev.classList.contains("bot")) prev.classList.add("cont");
    status.textContent=NAME+" is typing…"; scroll();
    return {remove:function(){ r.remove(); var p=log.lastElementChild; if(p&&p.classList.contains("bot")) p.classList.remove("cont"); status.textContent="Texas exam helper · online"; }};
  }
  function wait(ms){return new Promise(function(r){setTimeout(r,reduceMotion?0:ms);});}
  /* each line takes 1 to 2 seconds of "typing", longer lines a bit longer */
  function pause(text){return Math.max(1000,Math.min(2000,700+String(text).length*12));}
  function setBusy(b){busy=b;sendBtn.disabled=b;input.disabled=b;}
  function track(name,params){try{if(window.dash&&dash.track)dash.track(name,params||{});}catch(e){} try{if(window.gtag)gtag("event",name,params||{});}catch(e){}}
  function deliver(reply,prods,sugg,ctl,waited){
    var list=parts(reply), i=0, t=null;
    function next(){
      if(ctl&&ctl.stop){ if(t) t.remove(); return Promise.resolve(); }
      if(i>=list.length){ if(t) t.remove(); cards(prods); setChips(sugg); return Promise.resolve(); }
      var text=list[i++];
      if(!t) t=typing();
      return wait(i===1?Math.max(0,pause(text)-(waited||0)):pause(text)).then(function(){ if(ctl&&ctl.stop){ if(t) t.remove(); return; } t.remove(); t=null; bubble("bot",text,true); if(i<list.length) t=typing(); return next(); });
    }
    return next();
  }

  /* typed questions go to the AI */
  function send(text){
    text=(text||"").trim(); if(!text||busy) return;
    if(greetRun){ greetRun.stop=true; greetRun=null; render(false); }
    log.querySelectorAll(".ai-pickwrap").forEach(function(n){n.remove();}); setChips([]);
    st.messages.push({role:"user",content:text}); st.view.push({type:"user",text:text}); bubble("user",text,true);
    input.value=""; setBusy(true);
    var dots=null, t0=Date.now(), slow=setTimeout(function(){dots=typing();},120);
    track("ai_advisor_message",{search_term:text.slice(0,100)});
    var slots={trade:st.slots.trade||null,license:st.slots.license||null,want:(st.slots.want&&st.slots.want!=="help")?st.slots.want:null};
    fetch(ENDPOINT,{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({messages:st.messages.slice(-12),slots:slots,site:{brand:SITE.brand||"",fulfillment:SITE.fulfillment||"",phone:PHONE,base:new URL(S.BASE,location.href).href}})})
      .then(function(r){return r.json();})
      .then(function(d){
        clearTimeout(slow); if(dots) dots.remove();
        var reply=d.reply||"Sorry, I didn't get that. Can you say it another way?", prods=d.products||[], sugg=d.suggestions||[];
        var ns=d.slots||{}; ["trade","license","want"].forEach(function(k){ if(ns[k]) st.slots[k]=ns[k]; });
        var step=prods.length?"done":(st.slots.license?null:needStep(st.slots));
        st.messages.push({role:"assistant",content:reply+(prods.length?" [Shown: "+prods.map(function(x){var p=item(x.id);return p?p.cn+" "+p.tn:"";}).join("; ")+"]":"")});
        st.view.push({type:"bot",text:reply,products:prods,suggestions:sugg,step:step}); save();
        if(prods.length) track("ai_advisor_recommend",{products:prods.map(function(p){return p.id;}).join(","),mode:"chat"});
        return deliver(reply,prods,(step&&step!=="done")?[]:sugg,null,Date.now()-t0).then(function(){ if(step) showPicker(step); });
      })
      .catch(function(){clearTimeout(slow); if(dots) dots.remove(); bubble("bot","Sorry, I couldn't connect just now. You can still tap the buttons"+(PHONE?", or call us at "+PHONE:"")+".",true); var s=needStep(st.slots); if(s!=="done") showPicker(s);})
      .then(function(){setBusy(false);});
  }

  function chatMode(on,prefill){
    panel.hidden=!on; form.hidden=on; res.hidden=on; if(hint) hint.hidden=on;
    box.classList.toggle("ai-on",on);
    if(on){ ensureData(function(){ render(!prefill); if(prefill) send(prefill); }); track("ai_advisor_open",{}); }
    else { ov.dataset.aiSkip="1"; setTimeout(function(){S.q.focus();},20); }
  }
  aForm.addEventListener("submit",function(e){e.preventDefault();send(input.value);});
  box.addEventListener("click",function(e){
    if(e.target.closest("[data-ai-back]")){chatMode(false);return;}
    if(e.target.closest("[data-ai-reset]")){if(greetRun){greetRun.stop=true;greetRun=null;} st=fresh();save();render(true);return;}
    var pick=e.target.closest("[data-pick]"); if(pick){ var kind=pick.closest("[data-kind]").getAttribute("data-kind"); choose(kind,pick.getAttribute("data-pick"),pick.getAttribute("data-label")); return; }
    var chip=e.target.closest(".ai-chip"); if(chip){send(chip.textContent);}
  });
  /* opening search goes straight to Max. "Search instead" switches to the regular instant search until the page reloads. */
  new MutationObserver(function(){ if(!ov.hidden&&panel.hidden&&!ov.dataset.aiSkip) chatMode(true); }).observe(ov,{attributes:true,attributeFilter:["hidden"]});
  if(!ov.hidden&&!ov.dataset.aiSkip) chatMode(true);
  /* a question typed into the regular search box (several words, or ends with ?) goes to Max on Enter */
  form.addEventListener("submit",function(e){
    var t=S.q.value.trim();
    if(/\?$/.test(t)||t.split(/\s+/).length>=5){e.preventDefault();e.stopImmediatePropagation();S.q.value="";chatMode(true,t);}
  },true);
})();
