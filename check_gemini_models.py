# check_gemini_models.py
from google import genai
from config.settings import settings

print("Checking available Gemini models...\n")

try:
    client = genai.Client(api_key=settings.gemini_api_key)
    
    # List all available models
    models = client.models.list()
    
    print("✅ Available models:\n")
    
    for model in models:
        print(f"  • {model.name}")
    
    print("\n" + "="*60)
    print("We'll test which one works for generateContent")
    print("="*60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()