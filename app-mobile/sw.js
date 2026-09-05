const CACHE = "esprits-fn-v4-seasons";
const ASSETS = [
  "./",
  "./index.html",
  "./style.css",
  "./app.js",
  "./manifest.json",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)),
        ),
      ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);

  // Sprites images: reseau d'abord, cache en fallback.
  if (url.hostname === "spritelocker.com") {
    e.respondWith(
      caches.open(CACHE).then(async (cache) => {
        const cached = await cache.match(e.request);
        if (cached) return cached;
        try {
          const resp = await fetch(e.request);
          if (resp.ok) cache.put(e.request, resp.clone());
          return resp;
        } catch {
          return cached || new Response("", { status: 404 });
        }
      }),
    );
    return;
  }

  // Ressources locales de l'app: reseau d'abord pour capter les mises a jour,
  // puis cache en fallback hors-ligne.
  if (url.origin === self.location.origin) {
    e.respondWith(
      caches.open(CACHE).then(async (cache) => {
        try {
          const fresh = await fetch(e.request);
          if (fresh && fresh.ok) cache.put(e.request, fresh.clone());
          return fresh;
        } catch {
          const cached = await cache.match(e.request);
          return cached || new Response("", { status: 404 });
        }
      }),
    );
    return;
  }

  // Autres ressources externes: cache d'abord.
  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request)),
  );
});
