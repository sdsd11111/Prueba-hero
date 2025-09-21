#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
import json

# URL base del API
BASE_URL = "http://localhost:5000/api"

# Credenciales de administrador
ADMIN_CREDENTIALS = {
    "username": "La herencia",
    "password": "laherencia123"
}

# Datos de ejemplo de los platos
SAMPLE_PLATOS = [
    {
        "titulo": "Pechuga gratinada en salsa de champiñones",
        "descripcion": "Pechuga gratinada en salsa de champiñones con papas fritas, ensalada fresca, cheesecake de maracuyá y una bebida.",
        "precio": 13.00,
        "imagen_url": ""
    },
    {
        "titulo": "Hamburguesa La Herencia",
        "descripcion": "Hamburguesa de carne, cheddar y tocino con papas fritas, un cheesecake de maracuyá y una bebida.",
        "precio": 11.50,
        "imagen_url": ""
    },
    {
        "titulo": "Lasaña mixta",
        "descripcion": "Lasaña mixta acompañada de pan de ajo, una ensalada fresca, un cheesecake de maracuyá y una bebida.",
        "precio": 11.50,
        "imagen_url": ""
    }
]

def login():
    """Iniciar sesión como administrador"""
    print("🔐 Iniciando sesión como administrador...")
    
    response = requests.post(f"{BASE_URL}/login", json=ADMIN_CREDENTIALS)
    
    if response.status_code == 200:
        print("✅ Login exitoso")
        return response.cookies
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def create_plato(plato_data, cookies):
    """Crear un plato del día"""
    print(f"🍽️ Creando plato: {plato_data['titulo']}")
    
    response = requests.post(
        f"{BASE_URL}/admin/platos",
        json=plato_data,
        cookies=cookies
    )
    
    if response.status_code == 201:
        print(f"✅ Plato '{plato_data['titulo']}' creado exitosamente")
        return response.json()
    else:
        print(f"❌ Error creando plato: {response.status_code}")
        print(response.text)
        return None

def get_platos():
    """Obtener platos del día públicos"""
    print("📋 Obteniendo platos del día...")
    
    response = requests.get(f"{BASE_URL}/platos")
    
    if response.status_code == 200:
        platos = response.json()
        print(f"✅ Se encontraron {len(platos)} platos del día")
        return platos
    else:
        print(f"❌ Error obteniendo platos: {response.status_code}")
        return []

def main():
    print("🚀 Cargando datos de ejemplo para La Herencia")
    print("=" * 50)
    
    # Iniciar sesión
    cookies = login()
    if not cookies:
        print("❌ No se pudo iniciar sesión. Abortando.")
        return
    
    print()
    
    # Crear platos de ejemplo
    created_platos = []
    for plato_data in SAMPLE_PLATOS:
        plato = create_plato(plato_data, cookies)
        if plato:
            created_platos.append(plato)
        print()
    
    # Verificar platos creados
    print("🔍 Verificando platos creados...")
    platos = get_platos()
    
    print()
    print("📊 Resumen:")
    print(f"   • Platos creados: {len(created_platos)}")
    print(f"   • Platos activos: {len(platos)}")
    
    if platos:
        print("\n🍽️ Platos del día disponibles:")
        for i, plato in enumerate(platos, 1):
            print(f"   {i}. {plato['titulo']} - ${plato['precio']}")
    
    print("\n✅ Datos de ejemplo cargados exitosamente!")
    print("🌐 Puedes ver el resultado en: http://localhost:5000")
    print("🔧 Panel de administración: http://localhost:5000/admin.html")

if __name__ == "__main__":
    main()
