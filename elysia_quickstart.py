#!/usr/bin/env python3
"""
Elysia Quickstart Example
This script shows how to set up and use Elysia with your API keys
"""

import os
from dotenv import load_dotenv
from elysia import Tree, configure, preprocess

# Load environment variables from .env file
load_dotenv()

# Method 1: Using environment variables (recommended)
def setup_with_env():
    """
    This method assumes you have a .env file with:
    WCD_URL=https://xgsf87xst2qd5bjgbh54ba.c0.us-west3.gcp.weaviate.cloud
    WCD_API_KEY=<YOUR-WEAVIATE-API-KEY>
    OPENAI_API_KEY=sk-your-openai-key-here
    """
    tree = Tree()
    return tree

# Method 2: Using configure function (explicit)
def setup_with_configure():
    """
    This method explicitly sets all credentials in code
    """
    configure(
        # LLM Models
        base_model="gpt-4o-mini",
        base_provider="openai",
        complex_model="gpt-4o",
        complex_provider="openai",
        
        # API Keys
        openai_api_key="sk-your-openai-api-key-here",  # Replace with your actual OpenAI key
        
        # Weaviate credentials
        wcd_url="https://xgsf87xst2qd5bjgbh54ba.c0.us-west3.gcp.weaviate.cloud",
        wcd_api_key="<YOUR-WEAVIATE-API-KEY>"
    )
    
    tree = Tree()
    return tree

# Method 3: Using OpenRouter instead of OpenAI
def setup_with_openrouter():
    """
    This method uses OpenRouter for access to multiple models
    """
    configure(
        # LLM Models via OpenRouter
        base_model="openai/gpt-4o-mini",
        base_provider="openrouter",
        complex_model="openai/gpt-4o",
        complex_provider="openrouter",
        
        # API Keys
        openrouter_api_key="sk-or-your-openrouter-key-here",  # Replace with your actual OpenRouter key
        
        # Weaviate credentials
        wcd_url="https://xgsf87xst2qd5bjgbh54ba.c0.us-west3.gcp.weaviate.cloud",
        wcd_api_key="<YOUR-WEAVIATE-API-KEY>"
    )
    
    tree = Tree()
    return tree

# Example usage
def main():
    print("🚀 Elysia Quickstart")
    print("=" * 50)
    
    # Choose your setup method:
    # tree = setup_with_env()        # If using .env file
    tree = setup_with_configure()    # If hardcoding credentials
    # tree = setup_with_openrouter() # If using OpenRouter
    
    print("\n✅ Elysia configured successfully!")
    
    # Example 1: Simple calculation
    print("\n📊 Example 1: Simple calculation")
    response, objects = tree("What is 25 multiplied by 4?")
    print(f"Response: {response}")
    
    # Example 2: Query Weaviate data (if you have collections)
    print("\n🔍 Example 2: Query Weaviate")
    try:
        # First, check what collections exist
        from elysia.util.client import ClientManager
        client_manager = ClientManager()
        
        with client_manager.connect_to_client() as client:
            collections = client.collections.list_all()
            print(f"Available collections: {collections}")
            
            if collections:
                # If you have a collection, preprocess it first
                collection_name = collections[0]
                print(f"\nPreprocessing {collection_name}...")
                preprocess(collection_name)
                
                # Then query it
                response, objects = tree(
                    f"What data is in the {collection_name} collection?",
                    collection_names=[collection_name]
                )
                print(f"\nResponse: {response}")
            else:
                print("No collections found in your Weaviate cluster yet.")
                print("Upload some data to Weaviate first!")
    except Exception as e:
        print(f"Error connecting to Weaviate: {e}")
        print("Make sure your Weaviate credentials are correct.")

if __name__ == "__main__":
    # IMPORTANT: Before running this script:
    # 1. Get an OpenAI API key from https://platform.openai.com
    #    OR get an OpenRouter key from https://openrouter.ai
    # 2. Replace "sk-your-openai-api-key-here" with your actual key
    #    OR create a .env file with your keys
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set up your OpenAI or OpenRouter API key")
        print("   2. Your Weaviate cluster is active")
        print("   3. All required packages installed (pip install elysia-ai)")
