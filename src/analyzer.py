import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_data_for_json(data):
    """Convert datetime objects to strings for JSON serialization"""
    if isinstance(data, dict):
        return {k: clean_data_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data_for_json(item) for item in data]
    elif isinstance(data, datetime):
        return data.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return data

def analyze_markets(tradfi_data, crypto_data, onchain_data, news_data):
    """
    Send all market data to GPT-4o-mini for analysis
    Returns structured analysis of both markets
    """
    
    # Clean data to remove datetime objects
    tradfi_clean = clean_data_for_json(tradfi_data)
    crypto_clean = clean_data_for_json(crypto_data)
    onchain_clean = clean_data_for_json(onchain_data)
    news_clean = clean_data_for_json(news_data)
    
    # Format the data for the LLM
    context = f"""
Analyze today's market data. Be sharp and direct. Context matters - use the news to explain movements when relevant.

TRADITIONAL MARKETS:
{json.dumps(tradfi_clean, indent=2)}

CRYPTO MARKETS:
{json.dumps(crypto_clean, indent=2)}

ON-CHAIN DATA:
{json.dumps(onchain_clean, indent=2)}

RECENT NEWS (use this to explain market movements):
{json.dumps(news_clean, indent=2)}

Format:

**TODAY'S HEADLINE**
One sharp sentence with a laid back tone. If there's a clear catalyst in the news, reference it. Do not be overly vague.

**TRADITIONAL MARKETS**
What happened, why it matters, what's driving it. Reference news if it explains the move. Strong language when appropriate. 3-4 sentences.

**CRYPTO MARKETS**  
Same approach. If crypto is ignoring traditional market signals or news, point that out. 3-4 sentences.

**THE SPLIT**
How these markets are relating. If one is paying attention to reality and the other isn't, say so. 2-3 sentences.

**TOMORROW'S TELLS**
Specific things to watch based on today's pattern.

Voice guidelines:
- Sharp observations over decoration, with a touch of dry wit
- Confident and direct
- When something is obvious, state it plainly (that itself can be witty)
- Use precise language - call things what they are
- If markets are doing something irrational, you can note that
- Do not force being clever or funny - it should come naturally from the analysis
- Most sentences: straight analysis. Occasional sentence: makes someone nod and think "exactly."
"""

    print("🤖 Sending data to AI for analysis...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You're a sharp market analyst with a touch of sarcasm. Your wit comes from seeing patterns clearly and stating them confidently, not from jokes or analogies. You explain what happened and why. When markets do something that doesn't track with the news or fundamentals, you point it out plainly. You write with authority - the kind of analyst whose weekly notes people actually read because the observations are precise and occasionally cutting in their clarity, with a tone that doesn't take yourself too seriously."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            temperature=0.68,
            max_tokens=500
        )
        
        analysis = response.choices[0].message.content
        
        print("✅ AI analysis complete!\n")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")
        return None

if __name__ == "__main__":
    # Test with mock data
    print("Testing AI Analyzer with mock data\n")
    
    mock_tradfi = {
        'S&P 500': {'price': 5825.23, 'change': -1.2},
        'VIX': {'price': 18.45, 'change': 15.3}
    }
    
    mock_crypto = {
        'bitcoin': {'price': 62400, 'change_24h': -2.1},
        'ethereum': {'price': 3950, 'change_24h': 0.4}
    }
    
    mock_onchain = {
        'eth_price': 3950,
        'gas_prices': {'safe': '10', 'propose': '12', 'fast': '15'}
    }
    
    mock_news = [
        {'title': 'Fed signals rate hold', 'source': 'Reuters'},
        {'title': 'Bitcoin ETF sees inflows', 'source': 'Bloomberg'}
    ]
    
    analysis = analyze_markets(mock_tradfi, mock_crypto, mock_onchain, mock_news)
    
    if analysis:
        print("="*70)
        print("AI ANALYSIS:")
        print("="*70)
        print(analysis)