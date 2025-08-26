#!/usr/bin/env python3
"""
Script para probar la conexión directa con Weaviate Cloud
"""

import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth

# Cargar variables de entorno del archivo .env
load_dotenv()

def test_weaviate_direct_connection():
    """Prueba conexión directa con Weaviate usando tu script"""
    
    print("🔍 Probando conexión directa con Weaviate Cloud...")
    
    try:
        # Obtener credenciales de las variables de entorno
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        
        print(f"✅ URL: {weaviate_url}")
        print(f"✅ API Key: {weaviate_api_key[:20]}...")
        
        # Conectar a Weaviate Cloud
        print("\n🔌 Estableciendo conexión...")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
        )
        
        # Probar si está listo
        is_ready = client.is_ready()
        print(f"🚀 Cliente listo: {is_ready}")
        
        if is_ready:
            print("\n📊 Información del cluster:")
            
            # Obtener metadatos
            meta = client.get_meta()
            print(f"   Versión: {meta.get('version', 'N/A')}")
            
            # Listar colecciones
            collections = client.collections.list_all()
            print(f"   Colecciones: {len(collections)}")
            
            if collections:
                print("   Lista de colecciones:")
                for collection in collections:
                    print(f"     - {collection}")
            else:
                print("   No hay colecciones creadas aún")
        
        # Cerrar conexión
        client.close()
        return True
        
    except KeyError as e:
        print(f"❌ Error: Variable de entorno faltante: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("   Verifica que:")
        print("   1. La URL del cluster sea correcta")
        print("   2. La API key sea válida")
        print("   3. El cluster esté activo")
        return False

if __name__ == "__main__":
    print("🧪 Test de Conexión a Weaviate Cloud")
    print("=" * 50)
    
    success = test_weaviate_direct_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Conexión exitosa!")
        print("✅ Tu configuración de Weaviate está funcionando correctamente")
    else:
        print("❌ Hay problemas con la conexión")
        print("🔧 Revisa los mensajes de error arriba")
