"""
⚠️ ADVERTENCIA CRÍTICA: Este proyecto SOLO se ejecuta en Docker

NO ejecutes 'reflex run' directamente. Usa siempre:
docker compose -f docker-compose.desarrollo.yml up -d

Para más información, consulta DOCKER-ONLY.md
"""

import os
from dotenv import load_dotenv
load_dotenv()
import reflex as rx
import saltoestudia.theme as theme
from saltoestudia.database import engine  # Importar el engine

# Configuración de la aplicación completa
config = rx.Config(
    app_name="saltoestudia",
    db_url=str(engine.url),  # Usar la URL del engine importado
    api_url="http://localhost:8000",
    frontend_port=3000,  # Forzar puerto 3000 explícitamente
    backend_port=8000,   # Forzar puerto 8000 explícitamente
    style=theme.STYLESHEET,
    head_components=[
        rx.script(src="/chakra_color_mode_provider.js"),
        # CSS ESPECÍFICO para ocultar el footer "Built with Reflex"
        rx.html("""
        <style>
        /* Ocultar el footer "Built with Reflex" - TÉCNICAS MODERNAS */
        
        /* Selector principal: cualquier enlace que contenga reflex.dev */
        a[href*="reflex.dev"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: absolute !important;
            left: -9999px !important;
            top: -9999px !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            clip-path: inset(50%) !important;
        }
        
        /* Selector por clase CSS específica */
        .css-1qwptgo {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: absolute !important;
            left: -9999px !important;
            top: -9999px !important;
        }
        
        /* Selector por posición fija en la esquina inferior derecha */
        a[style*="position: fixed"][style*="bottom"][style*="right"],
        a[style*="position:fixed"][style*="bottom"][style*="right"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Selector por z-index alto */
        a[style*="z-index: 9998"],
        a[style*="z-index:9998"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Ocultar cualquier elemento que contenga el texto exacto */
        *:contains("Built with Reflex") {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* CSS más agresivo - ocultar elementos en la esquina inferior derecha */
        body > a:last-child,
        body > a:nth-last-child(1) {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        </style>
        
        <script>
        // JavaScript ROBUSTO para eliminar el footer "Built with Reflex"
        function removeReflexFooter() {
            // Método 1: Buscar y eliminar enlaces específicos de Reflex
            const reflexLinks = document.querySelectorAll('a[href*="reflex.dev"]');
            reflexLinks.forEach(link => {
                link.style.display = 'none';
                link.style.visibility = 'hidden';
                link.style.opacity = '0';
                link.style.pointerEvents = 'none';
                link.style.position = 'absolute';
                link.style.left = '-9999px';
                link.style.top = '-9999px';
                link.style.width = '0';
                link.style.height = '0';
                link.style.overflow = 'hidden';
            });
            
            // Método 2: Buscar elementos que contengan "Built with Reflex"
            const elements = document.querySelectorAll('*');
            elements.forEach(element => {
                if (element.textContent && element.textContent.includes('Built with Reflex')) {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                    element.style.opacity = '0';
                    element.style.pointerEvents = 'none';
                    element.style.position = 'absolute';
                    element.style.left = '-9999px';
                    element.style.top = '-9999px';
                }
            });
            
            // Método 3: Buscar elementos con posición fija en la esquina inferior derecha
            const fixedElements = document.querySelectorAll('a[style*="position: fixed"], a[style*="position:fixed"]');
            fixedElements.forEach(element => {
                const style = element.style.cssText || '';
                if (style.includes('bottom') && style.includes('right')) {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                    element.style.opacity = '0';
                    element.style.pointerEvents = 'none';
                }
            });
            
            // Método 4: Eliminar elementos por clase específica
            const cssElements = document.querySelectorAll('.css-1qwptgo');
            cssElements.forEach(element => {
                element.style.display = 'none';
                element.style.visibility = 'hidden';
                element.style.opacity = '0';
                element.style.pointerEvents = 'none';
            });
            
            // Método 5: Eliminar elementos por z-index
            const zIndexElements = document.querySelectorAll('a[style*="z-index: 9998"], a[style*="z-index:9998"]');
            zIndexElements.forEach(element => {
                element.style.display = 'none';
                element.style.visibility = 'hidden';
                element.style.opacity = '0';
                element.style.pointerEvents = 'none';
            });
        }
        
        // Ejecutar inmediatamente
        removeReflexFooter();
        
        // Ejecutar cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', removeReflexFooter);
        } else {
            removeReflexFooter();
        }
        
        // Ejecutar cuando la página esté completamente cargada
        window.addEventListener('load', removeReflexFooter);
        
        // Ejecutar periódicamente para asegurar que se elimine
        setInterval(removeReflexFooter, 250);
        
        // Observar cambios en el DOM para eliminar elementos que se agreguen dinámicamente
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    removeReflexFooter();
                }
            });
        });
        
        // Iniciar observación cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                observer.observe(document.body, { childList: true, subtree: true });
            });
        } else {
            observer.observe(document.body, { childList: true, subtree: true });
        }
        
        // Método adicional: Usar requestAnimationFrame para mayor eficiencia
        function removeReflexFooterRAF() {
            removeReflexFooter();
            requestAnimationFrame(removeReflexFooterRAF);
        }
        
        // Iniciar el loop de requestAnimationFrame
        requestAnimationFrame(removeReflexFooterRAF);
        </script>
        """),
    ],
    # Configuración de Tailwind - Deshabilitado porque no lo usamos
    tailwind=None,
    # Deshabilitar plugins problemáticos
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    # Deshabilitar el footer "Built with Reflex" por defecto
    footer=False,
    # Configuración de Vite para permitir el dominio de producción
    vite_config={
        "server": {
            "allowedHosts": "all",
            "host": "0.0.0.0",
            "port": 3000,
            "strictPort": True,
            "cors": True
        }
    },
    # Configuración de archivos estáticos para servir uploads
    # En Reflex, los archivos se sirven automáticamente desde assets/
    # No necesitamos static_dir, usamos assets/ como directorio estático por defecto
)
