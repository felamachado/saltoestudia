// Service Worker para Salto Estudia - Performance Optimization
const CACHE_NAME = 'saltoestudia-v2.0';
const STATIC_CACHE_NAME = 'saltoestudia-static-v2.0';
const DYNAMIC_CACHE_NAME = 'saltoestudia-dynamic-v2.0';

// === RECURSOS PARA CACHE ESTÁTICO ===
const STATIC_ASSETS = [
  '/',
  '/cursos',
  '/instituciones',
  '/info',
  '/assets/logo-redondo.webp',
  '/assets/logo-redondo.png',
  '/assets/favicon.ico',
  '/assets/logos/logo-cenur.png',
  '/assets/logos/logoutu.png',
];

// === RECURSOS PARA CACHE DINÁMICO ===
const DYNAMIC_CACHE_PATTERNS = [
  /\/_next\//,
  /\/assets\//,
  /\.(?:js|css|woff2?|ttf|eot)$/,
];

// === INSTALACIÓN DEL SERVICE WORKER ===
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker: Instalando...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then((cache) => {
        console.log('📦 Service Worker: Cacheando recursos estáticos');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Service Worker: Instalación completada');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Service Worker: Error en instalación:', error);
      })
  );
});

// === ACTIVACIÓN DEL SERVICE WORKER ===
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker: Activando...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            // Eliminar caches antiguos
            if (cacheName !== STATIC_CACHE_NAME && 
                cacheName !== DYNAMIC_CACHE_NAME) {
              console.log('🗑️ Service Worker: Eliminando cache antiguo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ Service Worker: Activación completada');
        return self.clients.claim();
      })
  );
});

// === ESTRATEGIA DE CACHE ===
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Solo cachear requests GET
  if (request.method !== 'GET') {
    return;
  }
  
  // No cachear WebSocket o APIs dinámicas
  if (url.pathname.startsWith('/_event') || 
      url.pathname.startsWith('/api/')) {
    return;
  }
  
  event.respondWith(
    handleRequest(request)
  );
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  try {
    // === ESTRATEGIA: CACHE FIRST para recursos estáticos ===
    if (DYNAMIC_CACHE_PATTERNS.some(pattern => pattern.test(url.pathname))) {
      return await cacheFirst(request, DYNAMIC_CACHE_NAME);
    }
    
    // === ESTRATEGIA: STALE WHILE REVALIDATE para páginas ===
    if (STATIC_ASSETS.includes(url.pathname)) {
      return await staleWhileRevalidate(request, STATIC_CACHE_NAME);
    }
    
    // === ESTRATEGIA: NETWORK FIRST para otras requests ===
    return await networkFirst(request, DYNAMIC_CACHE_NAME);
    
  } catch (error) {
    console.error('❌ Service Worker: Error en fetch:', error);
    
    // Fallback para páginas offline
    if (request.destination === 'document') {
      return await caches.match('/') || 
             new Response('Offline - Revisa tu conexión', {
               status: 503,
               statusText: 'Service Unavailable'
             });
    }
    
    return new Response('Resource not available offline', {
      status: 404,
      statusText: 'Not Found'
    });
  }
}

// === ESTRATEGIAS DE CACHE ===

async function cacheFirst(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  const networkResponse = await fetch(request);
  
  if (networkResponse.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, networkResponse.clone());
  }
  
  return networkResponse;
}

async function staleWhileRevalidate(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  const networkResponsePromise = fetch(request)
    .then(response => {
      if (response.ok) {
        const cache = caches.open(cacheName);
        cache.then(c => c.put(request, response.clone()));
      }
      return response;
    })
    .catch(() => cachedResponse);
  
  return cachedResponse || await networkResponsePromise;
}

async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    return cachedResponse || Promise.reject(error);
  }
}

// === MANEJO DE MENSAJES ===
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_CACHE_STATUS') {
    event.ports[0].postMessage({
      caches: CACHE_NAME,
      version: '2.0'
    });
  }
});

console.log('🎯 Service Worker v2.0 cargado - Optimizado para Salto Estudia'); 