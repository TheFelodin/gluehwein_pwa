#!/usr/bin/env python3
"""Neuer Barcode-Scanner für die PWA: eigene Kamera-Schleife plus ZXing (WebAssembly) statt html5-qrcode.
Benötigt zxing-scan.js und zxing_reader.wasm im selben Ordner wie index.html (liegen bei).
Aufruf: python scanner_patch.py index.html   (legt index.html.bak5 an)"""
import sys,shutil
pfad=sys.argv[1] if len(sys.argv)>1 else 'index.html'
roh=open(pfad,encoding='utf-8',newline='').read()
crlf='\r\n' in roh
src=roh.replace('\r\n','\n')
if 'id="scanVideo"' in src: sys.exit('Schon gepatcht.')
def rep(a,b):
    global src
    assert src.count(a)==1,'Anker nicht eindeutig gefunden: '+a[:70]
    src=src.replace(a,b)
def block(von,bis,neu):
    global src
    assert src.count(von)==1 and src.count(bis)==1,'Anker nicht eindeutig: '+von[:50]+' / '+bis[:50]
    a=src.index(von);b=src.index(bis)
    assert a<b,'Reihenfolge der Anker stimmt nicht'
    src=src[:a]+neu+src[b:]
A="let leser=null; // laufende Kamera, null = aus\nlet licht=false;\nconst FORMATE=['ean_13','ean_8','upc_a'];\nconst NATIV_NUTZEN=true; // false = immer ZXing (so verhält sich ein iPhone)\nconst nativOk=()=>NATIV_NUTZEN&&'BarcodeDetector' in window;\n\nfunction bildDaten(quelle,b,h,maxB){\n  const s=Math.min(1,maxB/Math.max(b,h)),cv=bildDaten.cv||(bildDaten.cv=document.createElement('canvas'));\n  cv.width=Math.round(b*s);cv.height=Math.round(h*s);\n  const c=cv.getContext('2d',{willReadFrequently:true});c.drawImage(quelle,0,0,cv.width,cv.height);\n  return c.getImageData(0,0,cv.width,cv.height);\n}\n\nasync function scannerStoppen(){\nconst l=leser;leser=null;\nif(l){l.lauf=false;l.strom.getTracks().forEach(t=>t.stop());$('#scanVideo').srcObject=null}\nif($('#scanDlg').open)$('#scanDlg').close();\n}\n\nasync function scannerStarten(){\nif(!navigator.mediaDevices?.getUserMedia)return toast('Dieses Gerät erlaubt keinen Kamerazugriff.');\nconst nativ=nativOk();\nif(!nativ&&typeof ZXScan==='undefined')return toast('Der Scanner konnte nicht geladen werden.');\n$('#scanMeldung').textContent='Starte Kamera …';\n$('#scanLicht').style.display='none';licht=false;\n$('#scanDlg').showModal();\ntry{\nconst strom=await navigator.mediaDevices.getUserMedia({audio:false,video:{facingMode:{ideal:'environment'},width:{ideal:1920},height:{ideal:1080}}});\nconst v=$('#scanVideo');v.srcObject=strom;await v.play();\nconst spur=strom.getVideoTracks()[0],l={strom,spur,lauf:true};leser=l;\ntry{await spur.applyConstraints({advanced:[{focusMode:'continuous'}]})}catch{}\ntry{if(spur.getCapabilities?.().torch)$('#scanLicht').style.display=''}catch{}\nconst det=nativ?new BarcodeDetector({formats:FORMATE}):null;\nif(!nativ)ZXScan.laden().catch(()=>{});\nconst s=spur.getSettings?.()||{},info=`${nativ?'Browser-Erkennung':'ZXing'}${s.width?`, Kamera ${s.width}×${s.height}`:''}`;\nconst start=performance.now();\n$('#scanMeldung').textContent=`Barcode quer, groß und ruhig halten (etwa 15 bis 25 cm). ${info}`;\nwhile(l.lauf){\nconst t0=performance.now();\nif(v.readyState>=2&&v.videoWidth){\nlet code=null;\ntry{\nif(det){const r=await det.detect(v);code=r.length?r[0].rawValue:null}\nelse code=await ZXScan.lesen(bildDaten(v,v.videoWidth,v.videoHeight,1600));\n}catch{}\nif(code&&/^\\d{8,14}$/.test(code)&&l.lauf){await scannerStoppen();barcodeGefunden(code);return}\n}\nif(t0-start>10000)$('#scanMeldung').textContent=`Nichts erkannt. Mehr Licht, Abstand ändern oder „Foto statt Live-Bild“ nutzen. ${info}`;\nawait new Promise(r=>setTimeout(r,Math.max(30,120-(performance.now()-t0))));\n}\n}catch{\nleser=null;\n$('#scanMeldung').textContent='Kamera nicht verfügbar. Prüfe die Berechtigung in den Browser- oder Systemeinstellungen oder tippe den Barcode ein.';\n}\n}\n\n"
B="$('#scanLicht').onclick=async()=>{\nif(!leser)return;\nlicht=!licht;\ntry{await leser.spur.applyConstraints({advanced:[{torch:licht}]})}catch{licht=!licht}\n};\n\nasync function barcodeAusBild(datei){\nlet bmp;try{bmp=await createImageBitmap(datei)}catch{return null}\ntry{\nif(nativOk()){\ntry{const r=await new BarcodeDetector({formats:FORMATE}).detect(bmp);if(r.length)return r[0].rawValue}catch{}\n}\nif(typeof ZXScan!=='undefined'){\nfor(const g of[2000,3200]){const code=await ZXScan.lesen(bildDaten(bmp,bmp.width,bmp.height,g));if(code)return code}\n}\n}catch{}\nreturn null;\n}\n\n"
rep('<script src="html5-qrcode.min.js"></script>','<script src="zxing-scan.js"></script>')
rep('<div id="leser" style="width:100%;min-height:200px"></div>','<div id="leser" style="position:relative;width:100%;overflow:hidden;border-radius:12px"><video id="scanVideo" playsinline muted autoplay style="display:block;width:100%;max-height:50vh;object-fit:cover;background:#000"></video><div style="position:absolute;left:6%;right:6%;top:28%;bottom:28%;border:2px solid rgba(255,255,255,.85);border-radius:8px;pointer-events:none"></div></div>')
block('let leser=null;','function barcodePruefen(){',A)
block("$('#scanLicht').onclick=async()=>{","$('#scanFoto').onclick=",B)
shutil.copyfile(pfad,pfad+'.bak5')
open(pfad,'w',encoding='utf-8',newline='').write(src.replace('\n','\r\n') if crlf else src)
print('Fertig. Sicherung:',pfad+'.bak5')
