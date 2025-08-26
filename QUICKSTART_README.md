# Elysia Quickstart Guide

I've created several files to help you get started with Elysia using your API keys:

## Files Created:

### 1. `env_template.txt`
A template for your `.env` file with your Weaviate credentials already filled in. You just need to add your OpenAI or OpenRouter API key.

**To use:**
```bash
# Copy the template to create your .env file
cp env_template.txt .env

# Edit .env and add your OpenAI API key
```

### 2. `test_elysia_setup.py`
A diagnostic script that checks if your environment is properly configured.

**Run this first:**
```bash
python test_elysia_setup.py
```

### 3. `minimal_example.py`
The simplest possible Elysia example with your credentials hardcoded. 
⚠️ **Remember to add your OpenAI API key!**

### 4. `elysia_quickstart.py`
A comprehensive example showing three different ways to configure Elysia:
- Using environment variables (.env file)
- Using the configure function
- Using OpenRouter instead of OpenAI

### 5. `quickstart_requirements.txt`
Install the required packages:
```bash
pip install -r quickstart_requirements.txt
```

## Quick Start Steps:

1. **Install dependencies:**
   ```bash
   pip install -r quickstart_requirements.txt
   ```

2. **Get your OpenAI API key:**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Create an API key
   - Copy it (starts with `sk-...`)

3. **Set up your environment:**
   ```bash
   # Create .env from template
   cp env_template.txt .env
   
   # Edit .env and add your OpenAI key
   # Replace sk-YOUR-OPENAI-KEY-HERE with your actual key
   ```

4. **Test your setup:**
   ```bash
   python test_elysia_setup.py
   ```

5. **Run the examples:**
   ```bash
   # Simple example
   python minimal_example.py
   
   # Full example
   python elysia_quickstart.py
   ```

## Your Credentials:

### ✅ Weaviate (Already configured):
- **URL**: `https://xgsf87xst2qd5bjgbh54ba.c0.us-west3.gcp.weaviate.cloud`
- **API Key**: `<YOUR-WEAVIATE-API-KEY>`

### ❌ Still needed:
- **OpenAI API Key**: Get from [platform.openai.com](https://platform.openai.com)
- OR **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai)

## Security Note:
⚠️ Since you've shared your Weaviate API key publicly, consider regenerating it in the Weaviate Cloud console for security.
