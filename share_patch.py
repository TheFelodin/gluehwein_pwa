#!/usr/bin/env python3
"""Share-Target für Android: Die App liest beim Start die vom Service Worker abgelegte Datei und zeigt den Import-Dialog.
Aufruf: python share_patch.py index.html   (legt index.html.bak3 an)"""
import sys,shutil
pfad=sys.argv[1] if len(sys.argv)>1 else 'index.html'
roh=open(pfad,encoding='utf-8',newline='').read()
crlf='\r\n' in roh
src=roh.replace('\r\n','\n')
if 'geteiltesPruefen' in src: sys.exit('Schon gepatcht.')
def rep(a,b):
    global src
    assert src.count(a)==1,'Anker nicht eindeutig gefunden: '+a[:70]
    src=src.replace(a,b)
FUNK='''/* ---------- Geteilte Datei empfangen (Android Share-Target) ---------- */
async function geteiltesPruefen(){
  if(!/[?&]geteilt=1/.test(location.search))return;
  history.replaceState(null,'',location.pathname);
  try{
    const c=await caches.open('gluehwein-share'),r=await c.match('geteilt.json');
    if(!r)return toast('Es wurde keine Datei empfangen.');
    const text=await r.text();await c.delete('geteilt.json');
    const x=await dateiLesen(text);
    if(!x||!x.liste.length)return toast('In der Datei wurden keine gültigen Bewertungen gefunden.');
    importZeigen(x);
  }catch{toast('Die geteilte Datei konnte nicht gelesen werden.')}
}

'''
rep('/* ---------- Start ---------- */',FUNK+'/* ---------- Start ---------- */')
rep('Promise.resolve(navigator.storage?.persist?.()).catch(()=>{});','geteiltesPruefen();\n  Promise.resolve(navigator.storage?.persist?.()).catch(()=>{});')
shutil.copyfile(pfad,pfad+'.bak3')
open(pfad,'w',encoding='utf-8',newline='').write(src.replace('\n','\r\n') if crlf else src)
print('Fertig. Sicherung:',pfad+'.bak3')
