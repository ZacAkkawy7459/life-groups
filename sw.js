/* Marriage Life Group — service worker.
 * Makes the site work offline once loaded. A dropped connection mid-session
 * never loses the page. Bump CACHE when you change the app files.
 */
var CACHE = "lg-v2";
var CORE = ["./", "./index.html", "./styles.css", "./groups.js",
  "./streams/marriage.js", "./streams/premarital.js", "./streams/parents-young.js",
  "./streams/parents-teens.js", "./streams/blended.js", "./streams/carers.js",
  "./streams/money.js", "./streams/grief.js"];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(CORE); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { if (k !== CACHE) return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var sameOrigin = new URL(req.url).origin === self.location.origin;

  if (sameOrigin) {
    // Network-first for our own files: online visitors always get the latest
    // deploy; the cache is only a fallback when offline.
    e.respondWith(
      fetch(req).then(function (res) {
        if (res && res.status === 200) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      }).catch(function () { return caches.match(req); })
    );
    return;
  }

  // Cross-origin (Google Fonts): cache-first, revalidate in the background.
  e.respondWith(
    caches.match(req).then(function (hit) {
      var net = fetch(req).then(function (res) {
        if (res && (res.status === 200 || res.type === "opaque")) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    })
  );
});
