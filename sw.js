const V = 'gluehwein-v4';
const SHARE = 'gluehwein-share';
const F = ['./', 'index.html', 'manifest.json', 'html5-qrcode.min.js', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(F)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(k => Promise.all(k.filter(x => x !== V && x !== SHARE).map(x => caches.delete(x))))
      .then(() => self.clients.claim())
  );
});

// Android: Eine im Teilen-Menü gewählte Datei kommt als POST an. Sie wird kurz zwischengespeichert,
// danach öffnet sich die App, liest sie aus und zeigt den Import-Dialog.
async function teilenAnnehmen(req) {
  try {
    const daten = await req.formData();
    const datei = daten.get('datei');
    if (datei && typeof datei !== 'string' && datei.size <= 30 * 1024 * 1024) {
      const c = await caches.open(SHARE);
      await c.put(
        new URL('geteilt.json', self.registration.scope).href,
        new Response(await datei.text(), { headers: { 'Content-Type': 'application/json' } })
      );
    }
  } catch (err) {}
  return Response.redirect(new URL('./?geteilt=1', self.registration.scope).href, 303);
}

self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);

  if (req.method === 'POST' && url.origin === self.location.origin && url.pathname.endsWith('/share-ziel')) {
    e.respondWith(teilenAnnehmen(req));
    return;
  }
  if (req.method !== 'GET') return;

  // Fremde Adressen (z. B. Open Food Facts) gehen direkt ins Netz, ohne Cache.
  if (url.origin !== self.location.origin) return;

  e.respondWith(
    fetch(req)
      .then(r => {
        if (r.ok) {
          const kopie = r.clone();
          caches.open(V).then(c => c.put(req, kopie));
        }
        return r;
      })
      .catch(async () => {
        const treffer = await caches.match(req, { ignoreSearch: true });
        if (treffer) return treffer;
        if (req.mode === 'navigate') return caches.match('index.html');
        return Response.error();
      })
  );
});
