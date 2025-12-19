"""
Quick script to check if COHERE_API_KEY environment variable is set
Run this to verify your environment setup before running the app
"""
import os
from dotenv import load_dotenv

def check_environment():
    """Check if required environment variables are set"""
    
    print("=" * 60)
    print("Environment Variable Check")
    print("=" * 60)
    
    # Load .env file if it exists (for local development)
    load_dotenv()
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"[OK] .env file found: {env_file}")
    else:
        print(f"[INFO] .env file not found: {env_file}")
        print("   (This is OK if using Hugging Face Spaces secrets)")
    
    print()
    
    # Check COHERE_API_KEY
    api_key = os.getenv("COHERE_API_KEY")
    
    if api_key:
        print(f"[OK] COHERE_API_KEY: FOUND")
        print(f"   Length: {len(api_key)} characters")
        
        # Show masked version for security
        if len(api_key) > 14:
            masked = api_key[:10] + "..." + api_key[-4:]
        else:
            masked = "***"
        print(f"   Preview: {masked}")
        
        # Check if it's a placeholder
        if api_key == "your_cohere_api_key_here" or api_key == "":
            print("   [WARNING] This looks like a placeholder value!")
            print("   Please set your actual Cohere API key")
            return False
        else:
            print("   Status: [OK] Valid key format")
            return True
    else:
        print("[ERROR] COHERE_API_KEY: NOT FOUND")
        print()
        print("To fix this:")
        print("1. Local Development:")
        print("   - Create .env file")
        print("   - Add: COHERE_API_KEY=your_actual_key_here")
        print()
        print("2. Hugging Face Spaces:")
        print("   - Go to Space Settings → Repository secrets")
        print("   - Add secret: COHERE_API_KEY")
        print("   - Value: your_actual_key_here")
        print()
        print("Get your API key from: https://dashboard.cohere.com/api-keys")
        return False

def check_all_cohere_vars():
    """Check all COHERE-related environment variables"""
    print()
    print("=" * 60)
    print("All COHERE-related Environment Variables")
    print("=" * 60)
    
    cohere_vars = {k: v for k, v in os.environ.items() if "COHERE" in k.upper()}
    
    if cohere_vars:
        for key, value in cohere_vars.items():
            if len(value) > 14:
                masked = value[:10] + "..." + value[-4:]
            else:
                masked = "***" if value else "(empty)"
            print(f"  {key}: {masked}")
    else:
        print("  No COHERE-related environment variables found")

if __name__ == "__main__":
    success = check_environment()
    check_all_cohere_vars()
    
    print()
    print("=" * 60)
    if success:
        print("[SUCCESS] Environment check passed! Your app should work correctly.")
    else:
        print("[FAILED] Environment check failed! Please fix the issues above.")
    print("=" * 60)

