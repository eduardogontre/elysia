#!/usr/bin/env python3
"""
Script para probar la conexión entre Elysia y Weaviate Cloud
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_weaviate_connection():
    """Prueba la conexión con Weaviate Cloud"""
    
    print("🔍 Verificando configuración...")
    
    # Verificar variables de entorno
    wcd_url = os.getenv("WCD_URL")
    wcd_api_key = os.getenv("WCD_API_KEY")
    
    if not wcd_url:
        print("❌ Error: WCD_URL no está configurada")
        return False
    
    if not wcd_api_key:
        print("❌ Error: WCD_API_KEY no está configurada")
        return False
    
    print(f"✅ WCD_URL: {wcd_url}")
    print(f"✅ WCD_API_KEY: {wcd_api_key[:10]}...")
    
    try:
        # Importar y probar Elysia
        from elysia.util.client import ClientManager
        
        print("\n🔌 Probando conexión con Weaviate...")
        
        # Crear cliente manager
        client_manager = ClientManager()
        
        if not client_manager.is_client:
            print("❌ Error: No se puede conectar al cliente de Weaviate")
            print("   Verifica que WCD_URL y WCD_API_KEY estén correctamente configuradas")
            return False
        
        # Probar conexión
        with client_manager.connect_to_client() as client:
            print("✅ Conexión exitosa con Weaviate Cloud!")
            
            # Listar colecciones existentes
            collections = client.collections.list_all()
            print(f"📊 Colecciones encontradas: {len(collections)}")
            
            if collections:
                print("   Colecciones:")
                for collection in collections[:5]:  # Mostrar solo las primeras 5
                    print(f"   - {collection}")
                if len(collections) > 5:
                    print(f"   ... y {len(collections) - 5} más")
            else:
                print("   No hay colecciones creadas aún")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar Elysia: {e}")
        print("   Asegúrate de que Elysia esté instalado: pip install -e .")
        return False
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("   Verifica que:")
        print("   1. La URL del cluster sea correcta")
        print("   2. La API key sea válida")
        print("   3. El cluster esté activo")
        return False

def test_llm_configuration():
    """Prueba la configuración de LLM"""
    
    print("\n🤖 Verificando configuración de LLM...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not openai_key and not openrouter_key:
        print("⚠️  Advertencia: No hay API keys de LLM configuradas")
        print("   Para usar Elysia completamente, necesitas al menos una de:")
        print("   - OPENAI_API_KEY")
        print("   - OPENROUTER_API_KEY")
        return False
    
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...")
    
    if openrouter_key:
        print(f"✅ OPENROUTER_API_KEY: {openrouter_key[:10]}...")
    
    return True

def main():
    """Función principal"""
    
    print("🚀 Probando configuración de Elysia + Weaviate Cloud")
    print("=" * 60)
    
    # Probar conexión Weaviate
    weaviate_ok = test_weaviate_connection()
    
    # Probar configuración LLM
    llm_ok = test_llm_configuration()
    
    print("\n" + "=" * 60)
    
    if weaviate_ok and llm_ok:
        print("🎉 ¡Todo configurado correctamente!")
        print("\n🔥 Puedes empezar a usar Elysia:")
        print("   from elysia import Tree")
        print("   tree = Tree()")
        print("   response, objects = tree('¿Qué colecciones tienes disponibles?')")
        
    elif weaviate_ok:
        print("✅ Weaviate está configurado correctamente")
        print("⚠️  Necesitas configurar al menos una API key de LLM para usar Elysia completamente")
        
    else:
        print("❌ Hay problemas con la configuración")
        print("   Revisa los mensajes de error arriba")

if __name__ == "__main__":
    main()
