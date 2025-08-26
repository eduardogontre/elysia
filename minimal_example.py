#!/usr/bin/env python3
"""
Minimal Elysia Example with Your API Keys
"""

from elysia import configure, Tree

# Configure Elysia with your credentials
configure(
    # Models (using OpenAI)
    base_model="gpt-4o-mini",
    base_provider="openai",
    complex_model="gpt-4o",
    complex_provider="openai",
    
    # Your Weaviate credentials
    wcd_url="https://xgsf87xst2qd5bjgbh54ba.c0.us-west3.gcp.weaviate.cloud",
    wcd_api_key="<YOUR-WEAVIATE-API-KEY>",
    
    # ⚠️ YOU NEED TO ADD YOUR OPENAI KEY HERE ⚠️
    openai_api_key="sk-REPLACE-WITH-YOUR-ACTUAL-OPENAI-KEY"
)

# Create an Elysia tree
tree = Tree()

# Use it!
response, objects = tree("What is 2 + 2?")
print(response)
