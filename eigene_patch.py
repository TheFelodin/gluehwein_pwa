#!/usr/bin/env python3
"""Import-Schalter „Das sind meine eigenen Bewertungen“ (Umzug von der Android-App in die PWA).
Aufruf: python eigene_patch.py index.html   (legt index.html.bak4 an)"""
import sys,shutil
pfad=sys.argv[1] if len(sys.argv)>1 else 'index.html'
roh=open(pfad,encoding='utf-8',newline='').read()
crlf='\r\n' in roh
src=roh.replace('\r\n','\n')
if 'impEigen' in src: sys.exit('Schon gepatcht.')
def rep(a,b):
    global src
    assert src.count(a)==1,'Anker nicht eindeutig gefunden: '+a[:70]
    src=src.replace(a,b)
# Dialog
rep('<div id="impText"></div>','<div id="impText"></div>\n<div class="zeile" id="impEigenZeile" style="display:none"><span>Das sind meine eigenen Bewertungen<br><small class="sub" id="impEigenInfo"></small></span><input type="checkbox" id="impEigen"></div>')
# Dialog-Logik
rep("$('#impJa').disabled=!an&&!backup;\noffenerImport={plaene,backup};",'''const zaehl={};for(const d of l)if(d.vonId)zaehl[d.vonId]=(zaehl[d.vonId]||0)+1;
const eigId=!backup?Object.keys(zaehl).sort((a,b)=>zaehl[b]-zaehl[a])[0]||null:null;
const meine=eigId?l.filter(d=>d.vonId===eigId):[];
const konv=meine.filter(d=>weine.some(t=>t.eintragId&&t.eintragId===d.eintragId&&t.von)).length;
const box=$('#impEigen'),zeigen=!!eigId&&(an>0||konv>0);
box.checked=false;$('#impEigenZeile').style.display=zeigen?'':'none';
if(zeigen){
const keine=!weine.some(w=>!w.von);
$('#impEigenInfo').textContent=`${meine.length} von ${l.length} stammen von ${meine[0].von?'„'+meine[0].von+'“':'derselben Person'}. `+(keine?'Deine Nutzer-ID wird auf deren ID gesetzt, so bleiben deine geteilten Bewertungen bei Freunden zugeordnet.':'Deine Nutzer-ID bleibt unverändert.');
}
const aktual=()=>{$('#impJa').disabled=!(an>0||backup||(box.checked&&konv>0))};
box.onchange=aktual;aktual();
offenerImport={plaene,backup,eigId:zeigen?eigId:null,eigName:zeigen?(meine[0].von||''):''};''')
rep("await anwenden(o.plaene,!!o.backup);",'''const eigen=!o.backup&&o.eigId&&$('#impEigen').checked?o.eigId:null,keineEigenen=!weine.some(w=>!w.von);
await anwenden(o.plaene,!!o.backup,eigen);
if(eigen){if(keineEigenen)speichere('nutzerId',eigen);if(o.eigName&&!meinName())speichere('name',o.eigName)}''')
# Anwenden: eigene Einträge ohne Absender speichern, auch bereits als „fremd“ vorhandene umwandeln
rep("async function anwenden(plaene,backupModus){\nfor(const {d,art,t} of plaene){\nif(art==='bekannt')continue;","async function anwenden(plaene,backupModus,eigId){\nfor(const {d,art,t} of plaene){\nconst mein=!!eigId&&d.vonId===eigId;\nif(art==='bekannt'&&!(mein&&t&&t.von))continue;")
rep("geaendert:d.geaendert||Date.now(),vonId:d.vonId,\nvon:backupModus?d.von:(d.von||(t?t.von:null)||'Freund')};","geaendert:d.geaendert||Date.now(),vonId:mein?null:d.vonId,\nvon:mein?null:backupModus?d.von:(d.von||(t?t.von:null)||'Freund')};")
rep("const w=art==='update'?{...t,...basis}:","const w=t?{...t,...basis}:")
shutil.copyfile(pfad,pfad+'.bak4')
open(pfad,'w',encoding='utf-8',newline='').write(src.replace('\n','\r\n') if crlf else src)
print('Fertig. Sicherung:',pfad+'.bak4')
