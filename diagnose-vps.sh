#!/bin/bash

echo "🔍 DIAGNÓSTICO DEL VPS - SALTO ESTUDIA"
echo "======================================"

# 1. Verificar si Docker está corriendo
echo "📋 1. Estado de Docker:"
if systemctl is-active --quiet docker; then
    echo "✅ Docker está corriendo"
else
    echo❌ Docker NO está corriendo"
    sudo systemctl start docker
    echo "🔄 Docker iniciado"
fi

# 2. Verificar si Traefik está corriendo
echo ""
echo "📋 2 Estado de Traefik:"
if docker ps | grep -q traefik; then
    echo "✅ Traefik está corriendo"
    docker ps | grep traefik
else
    echo ❌ Traefik NO está corriendo"
fi

# 3rificar si el contenedor de Salto Estudia está corriendo
echo ""
echo📋3stado del contenedor Salto Estudia:"
if docker ps | grep -q saltoestudia; then
    echo✅ Contenedor Salto Estudia está corriendo"
    docker ps | grep saltoestudia
else
    echo❌ Contenedor Salto Estudia NO está corriendo"
fi

#4Verificar logs del contenedor
echo cho "📋 4. Últimos logs del contenedor:"
if docker ps | grep -q saltoestudia; then
    echo📄 Últimas 20 líneas de logs:"
    docker logs --tail 20 saltoestudia-app
else
    echo "⚠️ No hay contenedor corriendo para ver logs"
fi

# 5. Verificar puertos
echocho📋 5 Puertos en uso:"
echo Puerto 80(HTTP):"
netstat -tlnp | grep :80 || echo "❌ Puerto80 está en usoecho Puerto443 (HTTPS):"
netstat -tlnp | grep :443 || echo "❌ Puerto 443 está en uso
echo "Puerto 3000rontend):"
netstat -tlnp | grep :3000 || echo❌ Puerto 300 está en uso
echo Puerto800Backend):"
netstat -tlnp | grep :8000 || echo❌ Puerto 80 no está en uso"

# 6. Verificar red de Docker
echo 
echo "📋 6. Redes de Docker:"
docker network ls | grep traefik

#7Verificar archivos del proyecto
echo "
echo "📋 7. Archivos del proyecto:"
if -d /srv/docker/saltoestudia]; then
    echo✅ Directorio del proyecto existe"
    ls -la /srv/docker/saltoestudia/
else
    echo❌ Directorio del proyecto NO existe"
fi

# 8. Verificar certificados SSL
echo "
echo "📋 8. Certificados SSL:"
if -d /srv/docker/traefik/certs]; then
    echo "✅ Directorio de certificados existe"
    ls -la /srv/docker/traefik/certs/
else
    echo "❌ Directorio de certificados NO existe
fi

#9st de conectividad
echo "
echo "📋9st de conectividad:
echo "Test localhost:30:"
curl -I http://localhost:30002/dev/null | head -1 || echo "❌ No responde localhost:3000
echo "Test localhost:80:"
curl -I http://localhost:80002/dev/null | head -1 || echo "❌ No responde localhost:8000

# 10.Verificar firewall
echo ""
echo 📋 10. Estado del firewall:"
if command -v ufw >/dev/null 2>&1n
    echoEstado UFW:"
    sudo ufw status
else
    echo "UFW no está instaladofi

echo 
echo "🔍 DIAGNÓSTICO COMPLETADO"
echo "==========================" 