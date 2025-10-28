"""Diagnostic script for OpenAI API issues."""

import os
import requests
from dotenv import load_dotenv

def test_openai_connection():
    """Test OpenAI API connection."""
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found (length: {len(api_key)})")
    
    # Test API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 10
    }
    
    try:
        print("🔄 Testing OpenAI API connection...")
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ OpenAI API connection successful")
            result = response.json()
            print(f"Response: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ OpenAI API request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Network connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_langchain():
    """Test LangChain OpenAI integration."""
    try:
        print("\n🔄 Testing LangChain...")
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.3,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        response = llm.invoke("Hello")
        print("✅ LangChain test successful")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LangChain test failed: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI API Diagnostic Tool")
    print("=" * 40)
    
    # Test 1: Direct API call
    api_works = test_openai_connection()
    
    # Test 2: LangChain
    langchain_works = test_langchain()
    
    print("\n" + "=" * 40)
    print("Summary:")
    print(f"Direct API: {'✅' if api_works else '❌'}")
    print(f"LangChain: {'✅' if langchain_works else '❌'}")
    
    if not api_works:
        print("\n🔧 Troubleshooting:")
        print("1. Check your OpenAI API key is valid")
        print("2. Check your internet connection")
        print("3. Check if OpenAI API is accessible from your network")
        print("4. Verify you have credits/quota available")
