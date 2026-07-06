/* New York, in Time — timeline engine */
(function(){
  'use strict';
  var EVENTS = (window.NYC_EVENTS || []).slice().sort(function(a,b){return a.sortKey-b.sortKey;});

  // ----- Era definitions (order + color) -----
  var ERAS = [
    {name:"Lenapehoking & New Amsterdam (pre-1664)", short:"New Amsterdam", rn:"I",   range:"pre-1664",     color:"#2f8a76"},
    {name:"Colonial & Revolutionary (1664–1783)",    short:"Colonial",     rn:"II",  range:"1664–1783",   color:"#b0503c"},
    {name:"Empire City Rising (1784–1897)",          short:"Empire City",  rn:"III", range:"1784–1897",   color:"#d8a94b"},
    {name:"Greater New York (1898–1945)",            short:"Greater NY",   rn:"IV",  range:"1898–1945",   color:"#4d79a8"},
    {name:"Modern Metropolis (1946–2000)",           short:"Modern",       rn:"V",   range:"1946–2000",   color:"#a4508b"},
    {name:"21st Century (2001–present)",             short:"21st C.",      rn:"VI",  range:"2001–now",    color:"#3aa0b0"}
  ];
  function eraIndex(name){for(var i=0;i<ERAS.length;i++){if(ERAS[i].name===name)return i;}return 2;}

  // Category palette
  var CATCOLOR = {
    "Founding & Colonial":"#2f8a76",
    "Politics & Government":"#b0503c",
    "Infrastructure & Building":"#d8a94b",
    "Immigration & People":"#4d79a8",
    "Disaster & Crisis":"#c85c4a",
    "Culture & Landmarks":"#a4508b",
    "Civil Rights & Protest":"#3aa0b0",
    "Economy & Money":"#7ba05b"
  };

  var $ = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  // ---------- HERO stats & stars ----------
  function buildStars(){
    var box=$("#stars"); if(!box) return; var n=70, html="";
    for(var i=0;i<n;i++){
      var seed=(i*97.13)%100, seed2=(i*53.7)%100, d=(i*0.137)%4;
      html+='<span class="star" style="left:'+seed.toFixed(2)+'%;top:'+(seed2*0.7).toFixed(2)+'%;animation-delay:'+d.toFixed(2)+'s"></span>';
    }
    box.innerHTML=html;
  }

  function heroStats(){
    if(!EVENTS.length) return;
    var years = EVENTS[EVENTS.length-1].sortKey - EVENTS[0].sortKey;
    var cats = {}; EVENTS.forEach(function(e){cats[e.category]=1;});
    var data=[
      {n:EVENTS.length, lbl:"Moments"},
      {n:years.toLocaleString()+"+", lbl:"Years spanned"},
      {n:ERAS.length, lbl:"Eras"},
      {n:Object.keys(cats).length, lbl:"Themes"}
    ];
    $("#heroStats").innerHTML = data.map(function(d){
      return '<div class="stat"><span class="n" data-count="'+d.n+'">'+d.n+'</span><span class="lbl">'+d.lbl+'</span></div>';
    }).join("");
    $("#footCount").textContent = EVENTS.length;
  }

  // ---------- Split hero title into letters ----------
  function animateTitle(){
    var t=$("#heroTitle"); if(!t) return;
    // wrap each visible character of the non-em lines already handled by CSS; add stagger to spans
    var em=t.querySelector('em');
    function wrap(node){
      var text=node.textContent, frag=document.createDocumentFragment(), idx=0;
      for(var i=0;i<text.length;i++){
        var ch=text[i];
        if(ch===' '){frag.appendChild(document.createTextNode(' '));continue;}
        var s=document.createElement('span'); s.className='l'; s.textContent=ch;
        s.style.animationDelay=(0.15+idx*0.045)+'s'; idx++;
        frag.appendChild(s);
      }
      node.textContent=''; node.appendChild(frag);
      return idx;
    }
    if(em) wrap(em);
    // second line "in Time" node is the last text — rebuild whole structure carefully
    // Rebuild: find text nodes after <br>
    var walker=[];
    Array.prototype.forEach.call(t.childNodes,function(n){
      if(n.nodeType===3 && n.textContent.trim()) walker.push(n);
    });
    var base=0.15+9*0.045;
    walker.forEach(function(node){
      var text=node.textContent, frag=document.createDocumentFragment(), idx=0;
      for(var i=0;i<text.length;i++){
        var ch=text[i];
        if(ch===' '){frag.appendChild(document.createTextNode(' '));continue;}
        var s=document.createElement('span'); s.className='l'; s.textContent=ch;
        s.style.animationDelay=(base+idx*0.05)+'s'; idx++;
        frag.appendChild(s);
      }
      node.parentNode.replaceChild(frag,node);
    });
  }

  // ---------- Build era pills ----------
  function buildPills(){
    var used = {}; EVENTS.forEach(function(e){used[e.era]=1;});
    $("#eraPills").innerHTML = ERAS.filter(function(er){return used[er.name];}).map(function(er,i){
      return '<button class="era-pill" data-era="'+er.name+'" style="--pc:'+er.color+'">'+er.short+'</button>';
    }).join("");
    $$(".era-pill").forEach(function(p){
      p.addEventListener('click',function(){
        var target=$('.era-anchor[data-era="'+p.dataset.era+'"]');
        if(target){ var y=target.getBoundingClientRect().top+window.scrollY-70; window.scrollTo({top:y,behavior:'smooth'}); }
      });
    });
  }

  // ---------- Build category chips ----------
  var activeCats = {};
  function buildChips(){
    var cats={}; EVENTS.forEach(function(e){cats[e.category]=1;});
    var list=Object.keys(cats);
    list.forEach(function(c){activeCats[c]=true;});
    var wrap=$("#catChips");
    list.forEach(function(c){
      var b=document.createElement('button');
      b.className='chip'; b.dataset.cat=c;
      b.innerHTML='<span class="sw" style="background:'+(CATCOLOR[c]||'#888')+'"></span>'+c;
      b.addEventListener('click',function(){
        activeCats[c]=!activeCats[c];
        b.classList.toggle('off',!activeCats[c]);
        applyFilters();
      });
      wrap.appendChild(b);
    });
  }

  // ---------- Render timeline ----------
  function render(){
    var host=$("#events"); if(!host) return;
    var html=""; var lastEra=null; var sideCounter=0;
    EVENTS.forEach(function(e,i){
      var er=ERAS[eraIndex(e.era)];
      if(e.era!==lastEra){
        html+='<div class="era-anchor" data-era="'+esc(e.era)+'" style="scroll-margin-top:80px"></div>';
        html+='<div class="era-band" style="--era:'+er.color+'">'
          +'<div class="rn">'+er.rn+'</div>'
          +'<div class="en">'+esc(er.name.replace(/\s*\(.*\)/,''))+'</div>'
          +'<div class="yr">'+esc(er.range)+'</div>'
          +'<div class="bar"></div></div>';
        lastEra=e.era; sideCounter=0;
      }
      var side = (sideCounter%2===0)?'left':'right'; sideCounter++;
      var conf = (e.confidence==='medium')?'<span class="conf medium">≈ approximate</span>':'';
      var color = CATCOLOR[e.category]||er.color;
      html+='<article class="event '+side+'" data-cat="'+esc(e.category)+'" data-search="'+esc((e.title+' '+e.blurb+' '+e.date).toLowerCase())+'" style="--era:'+er.color+'">'
        +'<span class="node"></span>'
        +'<div class="card" tabindex="0">'
          +'<div class="yr"><span class="ic">'+(e.icon||'•')+'</span><span>'+esc(String(e.date).match(/\d{3,4}|c\.\s?\d+/)?displayYear(e):e.date)+'</span></div>'
          +'<div class="date">'+esc(e.date)+'</div>'
          +'<h3>'+esc(e.title)+'</h3>'
          +'<p>'+esc(e.blurb)+'</p>'
          +'<div class="meta">'
            +'<span class="tag" style="background:'+color+'">'+esc(shortCat(e.category))+'</span>'
            + (e.sourceUrl?'<a class="src" href="'+esc(e.sourceUrl)+'" target="_blank" rel="noopener">▸ '+esc(e.source||'Source')+'</a>':'')
            + conf
          +'</div>'
        +'</div>'
      +'</article>';
    });
    host.innerHTML=html;
  }
  function displayYear(e){
    var m=String(e.date).match(/c\.\s?\d+|\d{3,4}/); return m?m[0]:e.date;
  }
  function shortCat(c){ return c.split(' & ')[0]; }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m];}); }

  // ---------- Scroll reveal ----------
  function observe(){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target);} });
    },{threshold:0.15, rootMargin:'0px 0px -8% 0px'});
    $$(".event").forEach(function(el){io.observe(el);});
  }

  // ---------- Spine fill, comet, progress, era tint ----------
  var timeline, spineFill, comet, atmos, controls, curEra=-1;
  function onScroll(){
    var st=window.scrollY, wh=window.innerHeight;
    var docH=document.documentElement.scrollHeight-wh;
    $("#progress").style.width=(st/docH*100)+'%';

    // controls appear after hero
    var heroH=$(".hero").offsetHeight;
    controls.classList.toggle('show', st>heroH*0.7);

    // spine fill relative to timeline box
    var r=timeline.getBoundingClientRect();
    var top=r.top+window.scrollY, h=timeline.offsetHeight;
    var prog=Math.min(1,Math.max(0,(st+wh*0.5-top)/h));
    spineFill.style.height=(prog*100)+'%';
    comet.style.top=(prog*h)+'px';

    // era tint by nearest active band
    var bands=$$(".era-band"); var active=0;
    for(var i=0;i<bands.length;i++){
      if(bands[i].getBoundingClientRect().top < wh*0.5) active=i;
    }
    if(active!==curEra){
      curEra=active;
      var color=bands[active] ? getComputedStyle(bands[active]).getPropertyValue('--era').trim() : ERAS[2].color;
      setEra(color, active);
    }
  }
  function setEra(color, idx){
    document.documentElement.style.setProperty('--era',color);
    document.documentElement.style.setProperty('--era-soft', hexA(color,.18));
    // highlight pill
    var eraName = ERAS[idx] ? ERAS[idx].name : null;
    $$(".era-pill").forEach(function(p){ p.classList.toggle('active', p.dataset.era===eraName); });
  }
  function hexA(hex,a){
    hex=hex.replace('#',''); if(hex.length===3){hex=hex.split('').map(function(c){return c+c;}).join('');}
    var r=parseInt(hex.substr(0,2),16),g=parseInt(hex.substr(2,2),16),b=parseInt(hex.substr(4,2),16);
    return 'rgba('+r+','+g+','+b+','+a+')';
  }

  // ---------- Filters ----------
  function applyFilters(){
    var q=($("#search").value||'').trim().toLowerCase();
    var shown=0;
    $$(".event").forEach(function(el){
      var catOk=activeCats[el.dataset.cat];
      var qOk=!q || el.dataset.search.indexOf(q)>=0;
      var ok=catOk&&qOk;
      el.classList.toggle('dim',!ok);
      el.style.pointerEvents=ok?'':'none';
      if(ok) shown++;
    });
  }

  // ---------- Guided tour ----------
  var touring=false, tourTimer=null, tourIdx=-1;
  function startTour(){
    if(touring){stopTour();return;}
    touring=true;
    $$("#tourBtn,#tourBtn2").forEach(function(b){b.classList.add('playing');b.textContent='⏸ Pause tour';});
    $("#tourBtn").textContent='⏸';
    toast('Tour started — sit back and scroll through history');
    tourIdx=-1; step();
    function step(){
      if(!touring) return;
      var evs=$$(".event:not(.dim)");
      tourIdx++;
      if(tourIdx>=evs.length){ stopTour(); toast('Tour complete — that’s four centuries.'); return; }
      var el=evs[tourIdx];
      var y=el.getBoundingClientRect().top+window.scrollY-window.innerHeight*0.4;
      window.scrollTo({top:y,behavior:'smooth'});
      el.classList.add('in');
      var card=el.querySelector('.card');
      card.style.transition='.4s'; card.style.borderColor='var(--brass-2)'; card.style.transform='translateY(-3px) scale(1.015)';
      setTimeout(function(){ if(card){card.style.borderColor='';card.style.transform='';} },2600);
      tourTimer=setTimeout(step,3000);
    }
  }
  function stopTour(){
    touring=false; clearTimeout(tourTimer);
    $$("#tourBtn2").forEach(function(b){b.classList.remove('playing');b.textContent='▶ Play the tour';});
    var tb=$("#tourBtn"); tb.classList.remove('playing'); tb.textContent='▶';
  }

  // ---------- Toast ----------
  var toastTimer;
  function toast(msg){
    var t=$("#toast"); t.textContent=msg; t.classList.add('show');
    clearTimeout(toastTimer); toastTimer=setTimeout(function(){t.classList.remove('show');},3200);
  }

  // ---------- Sources modal ----------
  function buildModal(){
    $("#srcList").innerHTML = EVENTS.map(function(e){
      var y=String(e.date);
      return '<li><span class="y">'+esc(y.match(/c\.\s?\d+|\d{3,4}/)?y.match(/c\.\s?\d+|\d{3,4}/)[0]:y)+'</span>'
        +'<span>'+esc(e.title)+' — '
        +(e.sourceUrl?'<a href="'+esc(e.sourceUrl)+'" target="_blank" rel="noopener">'+esc(e.source||'source')+'</a>':esc(e.source||''))
        +'</span></li>';
    }).join("");
  }
  function openModal(){$("#modalBg").classList.add('open');document.body.style.overflow='hidden';}
  function closeModal(){$("#modalBg").classList.remove('open');document.body.style.overflow='';}

  // ---------- Wire up ----------
  function wire(){
    controls=$("#controls"); timeline=$("#timeline"); spineFill=$("#spineFill"); comet=$("#comet");

    $("#filterBtn").addEventListener('click',function(){$("#filters").classList.toggle('open');});
    $("#search").addEventListener('input',applyFilters);
    $("#tourBtn").addEventListener('click',startTour);
    $("#tourBtn2").addEventListener('click',startTour);
    // stop tour when user scrolls manually
    var lastY=window.scrollY, ticking=false;
    window.addEventListener('scroll',function(){
      if(!ticking){requestAnimationFrame(function(){onScroll();ticking=false;});ticking=true;}
      if(touring && Math.abs(window.scrollY-lastY)>window.innerHeight*1.5){/* jump = ok */}
      lastY=window.scrollY;
    },{passive:true});

    ['#srcBtn','#srcBtn2','#srcBtn3'].forEach(function(id){
      var el=$(id); if(el) el.addEventListener('click',function(ev){ev.preventDefault();openModal();});
    });
    $("#modalClose").addEventListener('click',closeModal);
    $("#modalBg").addEventListener('click',function(e){if(e.target===$("#modalBg"))closeModal();});
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'){closeModal();stopTour();}
      if(e.key==='/'&&document.activeElement!==$("#search")){e.preventDefault();$("#filters").classList.add('open');$("#search").focus();}
    });
    onScroll();
  }

  // ---------- Init ----------
  function init(){
    if(!EVENTS.length){
      $("#events").innerHTML='<p style="text-align:center;color:var(--muted)">Loading the archive…</p>';
      return;
    }
    buildStars(); heroStats(); animateTitle(); buildPills(); buildChips();
    render(); observe(); buildModal(); wire();
  }
  if(document.readyState!=='loading') init(); else document.addEventListener('DOMContentLoaded',init);
})();
