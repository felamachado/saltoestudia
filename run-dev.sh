#!/bin/bash
# Script para ejecutar Salto Estudia en modo desarrollo (con hot-reload)
# Reemplaza: docker-compose up

echo "🚀 SALTO ESTUDIA - MODO DESARROLLO"
echo "=================================="
echo "Hot-reload: ✅ Activo"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""

# Función para limpiar puertos ocupados
clean_ports() {
    echo "🧹 Limpiando puertos 3000 y 8000..."
    
    # Matar procesos que puedan estar usando los puertos
    sudo lsof -ti:3000 | xargs -r sudo kill -9 2>/dev/null || true
    sudo lsof -ti:8000 | xargs -r sudo kill -9 2>/dev/null || true
    
    # Esperar un momento para que los puertos se liberen
    sleep 2
    
    echo "✅ Puertos limpiados"
}

# Función para verificar si la aplicación está respondiendo
check_app_health() {
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Verificando que la aplicación esté respondiendo..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
            echo "✅ Aplicación respondiendo correctamente en puerto 3000"
            return 0
        fi
        
        echo "⏳ Intento $attempt/$max_attempts - Esperando que la aplicación se inicie..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ La aplicación no está respondiendo después de $max_attempts intentos"
    return 1
}

# Función para reiniciar el contenedor si es necesario
restart_container() {
    echo "🔄 Reiniciando contenedor..."
    docker restart saltoestudia-app
    sleep 5
    
    if check_app_health; then
        echo "✅ Contenedor reiniciado exitosamente"
        return 0
    else
        echo "❌ Problema persistente después del reinicio"
        return 1
    fi
}

# Limpiar puertos antes de empezar
clean_ports

# Detener contenedor anterior si existe
docker stop saltoestudia-app 2>/dev/null || true
docker rm saltoestudia-app 2>/dev/null || true

# Construir imagen
echo "📦 Construyendo imagen..."
docker build -t saltoestudia .

# Ejecutar con hot-reload (montando volúmenes)
echo "🔄 Iniciando con hot-reload..."
docker run -d \
  --name saltoestudia-app \
  --network host \
  -v "$(pwd)":/app \
  -v "$(pwd)/data":/app/data \
  --env-file .env 2>/dev/null || docker run -d \
  --name saltoestudia-app \
  --network host \
  -v "$(pwd)":/app \
  -v "$(pwd)/data":/app/data \
  saltoestudia

# Esperar un momento para que el contenedor se inicie
sleep 5

# Verificar que la aplicación esté respondiendo
if check_app_health; then
    echo "✅ Salto Estudia ejecutándose en modo desarrollo"
    echo "Puedes editar el código y los cambios se aplicarán automáticamente"
    echo ""
    echo "Para ver logs: docker logs -f saltoestudia-app"
    echo "Para detener: docker stop saltoestudia-app"
else
    echo "❌ Problema detectado. Intentando reiniciar el contenedor..."
    
    if restart_container; then
        echo "✅ Problema resuelto después del reinicio"
    else
        echo "❌ Problema persistente. Mostrando logs del contenedor:"
        docker logs saltoestudia-app
        echo ""
        echo "💡 Soluciones posibles:"
        echo "   1. Verificar que no haya otros servicios usando los puertos 3000/8000"
        echo "   2. Reiniciar Docker: sudo systemctl restart docker"
        echo "   3. Verificar logs en tiempo real: docker logs -f saltoestudia-app"
        echo "   4. Probar acceso directo: curl http://localhost:3000"
    fi
fi 