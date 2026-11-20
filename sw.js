const V = 'gluehwein-v2';
const F = ['./', 'index.html', 'manifest.json', 'html5-qrcode.min.js', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(F)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(k => Promise.all(k.filter(x => x !== V).map(x => caches.delete(x))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  // Fremde Adressen (z. B. Open Food Facts) gehen direkt ins Netz, ohne Cache.
  if (new URL(req.url).origin !== self.location.origin) return;

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