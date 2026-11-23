#!/usr/bin/env python3
"""Fügt Statusleisten-Streifen, iOS-Hinweis und Adventskalender in die Glühwein-PWA ein.
Aufruf:  python advent_patch.py index.html     (legt index.html.bak an)"""
import sys,shutil
pfad=sys.argv[1] if len(sys.argv)>1 else 'index.html'
roh=open(pfad,encoding='utf-8',newline='').read()
crlf='\r\n' in roh
src=roh.replace('\r\n','\n')
if 'id="advent"' in src: sys.exit('Schon gepatcht (Adventskalender vorhanden).')
def rep(a,b):
    global src
    assert src.count(a)==1,'Anker nicht eindeutig gefunden: '+a[:60]
    src=src.replace(a,b)
ADVENT_JS='/* ---------- Adventskalender ---------- */\nconst ADVENT_TESTTAG=0; // Zum Testen einen Tag von 1 bis 24 eintragen, vor dem Verteilen wieder 0\nconst adventsTag=()=>{if(ADVENT_TESTTAG>0)return Math.min(ADVENT_TESTTAG,24);const d=new Date(),m=d.getMonth()+1;return m===12?Math.min(d.getDate(),24):m===1&&d.getDate()<=6?24:0};\nconst adventJahr=()=>{const d=new Date();return d.getMonth()===0?d.getFullYear()-1:d.getFullYear()};\nconst adventKey=t=>ADVENT_TESTTAG>0?\'test-\'+t:adventJahr()+\'-\'+t;\nconst adventDatum=t=>ADVENT_TESTTAG>0?new Date():new Date(adventJahr(),11,t);\nconst adventOffen=()=>new Set(store(\'adventOffen\',[]));\nconst istTag=(ms,d)=>{const x=new Date(ms);return x.getFullYear()===d.getFullYear()&&x.getMonth()===d.getMonth()&&x.getDate()===d.getDate()};\nconst eigene=()=>weine.filter(w=>!w.von);\nconst am=(d,f)=>eigene().some(w=>istTag(w.geaendert||0,d)&&f(w));\nconst SYM={Aufgabe:\'🎯\',Fakt:\'📖\',Tipp:\'💡\'},ARTF={Aufgabe:\'#8E1B3A\',Fakt:\'#1E5FA8\',Tipp:\'#2E6B3F\'};\nconst sym=a=>SYM[a]||\'✨\';\nconst ADV=[\n[\'Aufgabe\',\'Willkommen im Advent! Bewerte heute einen Glühwein.\',d=>am(d,()=>true)],\n[\'Fakt\',\'Schon die Römer würzten Wein mit Honig und Gewürzen. Der Vorläufer des Glühweins ist also rund 2000 Jahre alt.\'],\n[\'Aufgabe\',\'Füge heute bei einer Bewertung ein Foto hinzu.\',d=>am(d,w=>!!w.bild)],\n[\'Tipp\',\'Glühwein sollte nicht kochen. Ideal sind etwa 60 bis 70 °C, sonst verfliegen Alkohol und Aroma.\'],\n[\'Aufgabe\',\'Schreibe heute einen Kommentar zu einem Glühwein.\',d=>am(d,w=>!!(w.kommentar||\'\').trim())],\n[\'Fakt\',\'In der EU ist Glühwein gesetzlich geregelt: Er besteht aus gewürztem Wein und hat zwischen 7 und 14,5 Prozent Alkohol.\'],\n[\'Aufgabe\',\'Trage heute bei einer Bewertung den Preis ein. So findest du den Preis-Leistungs-Sieger.\',d=>am(d,w=>w.preis!=null)],\n[\'Tipp\',\'Nimm Zimtstangen statt Zimtpulver, dann bleibt dein Glühwein klar.\'],\n[\'Idee\',\'Probiere heute einen weißen Glühwein. Er schmeckt oft fruchtiger und heller.\'],\n[\'Aufgabe\',\'Bewerte heute zwei Glühweine am selben Tag.\',d=>eigene().filter(w=>istTag(w.geaendert||0,d)).length>=2],\n[\'Fakt\',\'Alkohol erweitert die Blutgefäße. Die Haut fühlt sich warm an, der Körper kühlt aber eher schneller aus.\'],\n[\'Aufgabe\',\'Scanne heute einen Barcode und lass Name und Bild automatisch ausfüllen.\',d=>am(d,w=>!!w.barcode)],\n[\'Tipp\',\'Orangenscheiben nur kurz mitziehen lassen. Die weiße Haut der Schale kann sonst bitter werden.\'],\n[\'Aufgabe\',\'Hast du Glühwein von mindestens drei verschiedenen Händlern bewertet?\',()=>new Set(eigene().map(w=>(w.haendler||\'\').trim().toLowerCase()).filter(Boolean)).size>=3],\n[\'Fakt\',\'Bei der Feuerzangenbowle tropft brennender, rumgetränkter Zuckerhut in den heißen Rotwein.\'],\n[\'Idee\',\'Teile heute eine Bewertung mit einem Freund. Gemeinsam schmeckt Glühwein besser.\'],\n[\'Aufgabe\',\'Vergib heute mindestens vier Tassen. Welcher Glühwein hat es verdient?\',d=>am(d,w=>w.wertung>=4)],\n[\'Fakt\',\'Glühwein gibt es in vielen Ländern: In Schweden heißt er Glögg, in Frankreich vin chaud.\'],\n[\'Aufgabe\',\'Bewerte heute einen Glühwein von einem Händler, bei dem du noch nichts bewertet hast.\',d=>{const m=eigene();return m.some(w=>istTag(w.geaendert||0,d)&&(w.haendler||\'\').trim()&&!m.some(o=>o.id<w.id&&(o.haendler||\'\').toLowerCase()===w.haendler.toLowerCase()))}],\n[\'Tipp\',\'Zucker oder Honig erst am Ende dazugeben und abschmecken. So wird der Glühwein nicht zu süß.\'],\n[\'Aufgabe\',\'Hast du heute einen Glühwein mit fünf Tassen gefunden?\',d=>am(d,w=>w.wertung>=5)],\n[\'Fakt\',\'Auf vielen Weihnachtsmärkten ist die Glühweintasse ein Sammlerstück. Manche Städte bringen jedes Jahr ein neues Motiv heraus.\'],\n[\'Idee\',\'Schau dir deine Rangliste an und wähle den „Glühwein des Jahres“.\'],\n[\'Idee\',\'Frohe Weihnachten! Dein Adventskalender ist komplett. Trinke heute eine Tasse auf deinen Lieblingsglühwein. Prost!\']\n];\nfunction adventKopf(){\n  const t=adventsTag(),an=deko()&&t>0;\n  $(\'#adventBtn\').style.display=an?\'\':\'none\';\n  const offen=an&&(ADVENT_TESTTAG>0||new Date().getMonth()===11)&&!adventOffen().has(adventKey(t));\n  $(\'#adHinweis\').textContent=offen?`🎁 Türchen ${t} wartet auf dich!`:\'\';\n}\nfunction adventRaster(){\n  const heute=adventsTag(),offen=adventOffen(),G=$(\'#tgrid\'),FA=[\'var(--pr)\',\'#2E6B3F\',\'#b07a1c\'];let n=0;G.innerHTML=\'\';\n  for(let t=1;t<=24;t++){\n    const o=offen.has(adventKey(t)),[art,,pr]=ADV[t-1];if(o)n++;\n    const er=o&&pr?pr(adventDatum(t)):null,b=document.createElement(\'button\');\n    b.className=\'tf\'+(o?\' auf\':\'\')+(t>heute?\' zu\':\'\');\n    b.style.setProperty(\'--fa\',FA[(t-1)%3]);b.style.setProperty(\'--ak\',ARTF[art]||\'#8A5A00\');\n    b.innerHTML=`<span class="hint">${o?`<i>${sym(art)}</i>${er===null?\'\':er?\'✅\':\'offen\'}`:\'⭐\'}</span><span class="tuer">${t}</span>`;\n    b.onclick=()=>adventKlick(t,b);G.append(b);\n  }\n  $(\'#adZahl\').textContent=`${n} von 24 Türchen geöffnet`;\n}\nfunction adventZeigen(t){\n  const [art,text,pr]=ADV[t-1],er=pr?pr(adventDatum(t)):null;\n  $(\'#adT\').textContent=\'Türchen \'+t;$(\'#adArt\').textContent=`${sym(art)} ${art}`;$(\'#adText\').textContent=text;\n  $(\'#adStatus\').textContent=er===null?\'\':er?\'✅ Erledigt\':\'Noch nicht erledigt\';\n  $(\'#adventDlg\').showModal();\n}\nfunction adventKlick(t,b){\n  if(t>adventsTag())return toast(`Türchen ${t} ist erst am ${t}. Dezember dran.`);\n  const k=adventKey(t),o=adventOffen();\n  if(o.has(k))return adventZeigen(t);\n  o.add(k);speichere(\'adventOffen\',[...o]);b.classList.add(\'auf\');\n  setTimeout(()=>{adventZeigen(t);adventRaster();adventKopf()},550);\n}\nfunction adventAnsicht(an){\n  $(\'#haupt\').style.display=an?\'none\':\'\';$(\'#advent\').style.display=an?\'block\':\'none\';\n  if(an){$(\'#adTest\').style.display=ADVENT_TESTTAG>0?\'\':\'none\';adventRaster()}\n  window.scrollTo(0,0);\n}\n$(\'#adventBtn\').onclick=$(\'#adHinweis\').onclick=()=>adventAnsicht(true);\n$(\'#adZurueck\').onclick=()=>{adventAnsicht(false);liste()};\n$(\'#adClose\').onclick=()=>$(\'#adventDlg\').close();\n$(\'#adTest\').onclick=()=>{speichere(\'adventOffen\',[...adventOffen()].filter(k=>!k.startsWith(\'test-\')));adventRaster();adventKopf()};\ndocument.addEventListener(\'visibilitychange\',()=>{if(!document.hidden){kopf();adventKopf()}});\n\n/* ---------- Hinweis „Zum Home-Bildschirm“ (nur iOS im Browser) ---------- */\n(()=>{\n  const ios=/iphone|ipad|ipod/i.test(navigator.userAgent)||(navigator.platform===\'MacIntel\'&&navigator.maxTouchPoints>1);\n  const app=navigator.standalone===true||matchMedia(\'(display-mode: standalone)\').matches;\n  if(ios&&!app&&!store(\'iosHinweisZu\',false))$(\'#iosHint\').hidden=false;\n  $(\'#iosHintZu\').onclick=()=>{$(\'#iosHint\').hidden=true;speichere(\'iosHinweisZu\',true)};\n})();\n'
# --- CSS ---
rep('</style>','''body::before{content:"";position:fixed;top:0;left:0;right:0;height:env(safe-area-inset-top);background:#7a1c2c;z-index:5}
.hinweis{display:flex;align-items:center;gap:8px;margin:4px 16px;padding:8px 8px 8px 14px;background:var(--chip);border-radius:12px;font-size:14px;position:relative;z-index:1}
.hinweis[hidden]{display:none}.hinweis span{flex:1}.hinweis .ib{font-size:18px;padding:6px}
#advent{display:none;position:relative;z-index:1;max-width:640px;margin:0 auto;padding:0 16px calc(24px + env(safe-area-inset-bottom))}
#advent h2{display:flex;align-items:center;margin:8px 0;font-size:22px}
#tgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.tf{position:relative;aspect-ratio:1;border:0;padding:0;border-radius:12px;overflow:hidden;background:var(--chip)}
.tf .hint{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;font-weight:600;background:var(--chip)}
.tf .hint i{font-style:normal;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-size:20px;background:color-mix(in srgb,var(--ak) 25%,transparent)}
.tf .tuer{position:absolute;inset:0;display:grid;place-items:center;background:var(--fa);color:#fff;font-size:24px;font-weight:700;transform-origin:left center;transform:perspective(300px) rotateY(0);transition:transform .5s;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.tf.auf .tuer{transform:perspective(300px) rotateY(-105deg)}.tf.zu .tuer{opacity:.5}
</style>''')

# --- HTML ---
rep('<div class="cd" id="cd"></div>','<div class="cd" id="cd"></div><div class="cd" id="adHinweis" style="cursor:pointer"></div>')
rep('<button class="ib" id="menuBtn" aria-label="Menü">⋮</button>','<button class="ib" id="adventBtn" aria-label="Adventskalender" style="display:none">🎁</button><button class="ib" id="menuBtn" aria-label="Menü">⋮</button>')
rep('</header>','''</header>
  <div class="hinweis" id="iosHint" hidden><span>Tippe auf Teilen (□↑) und wähle „Zum Home-Bildschirm“. Starte die App dann von dort, nur so bleiben deine Bewertungen dauerhaft gespeichert. Die installierte App beginnt mit einer leeren Liste.</span><button class="ib" id="iosHintZu" aria-label="Schließen">✕</button></div>''')
rep('<div id="gross">','''<section id="advent">
  <h2><button class="ib" id="adZurueck" aria-label="Zurück">←</button><span>Adventskalender</span></h2>
  <div class="sub" id="adZahl"></div>
  <div class="sub">🎯 Aufgabe · 📖 Fakt · 💡 Tipp · ✨ Idee · ✅ erledigt</div>
  <button class="btn t" id="adTest" style="display:none">Testtürchen zurücksetzen</button>
  <div id="tgrid"></div>
</section>
<dialog id="adventDlg">
  <h3 id="adT"></h3><div class="sub" id="adArt" style="font-weight:600"></div>
  <p id="adText"></p><div id="adStatus" style="font-weight:600"></div>
  <div class="aktionen"><button class="btn" id="adClose">Schließen</button></div>
</dialog>
<div id="gross">''')

rep('function liste(){\n  kopf();','function liste(){\n  kopf();adventKopf();')

js=ADVENT_JS
rep('/* ---------- Start ---------- */',js+'\n/* ---------- Start ---------- */')


shutil.copyfile(pfad,pfad+'.bak')
open(pfad,'w',encoding='utf-8',newline='').write(src.replace('\n','\r\n') if crlf else src)
print('Fertig. Sicherung:',pfad+'.bak')
