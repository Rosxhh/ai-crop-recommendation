const CACHE_NAME = 'agricore-pwa-cache-v1';
const urlsToCache = [
  '/',
  '/yield/',
  '/recommend/',
  '/soil/',
  '/chatbot/',
  '/weather/',
  // Note: we can't cache external CDNs offline easily without CORS, but we'll focus on the HTML pages.
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', event => {
  // Try network first, then cache if offline.
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
