"""Quick test of OpenAI API key."""

import openai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Testing OpenAI API key...")
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Say hello in one word'}],
        max_tokens=5,
        timeout=5
    )
    
    print(f"✅ API Key works! Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")

