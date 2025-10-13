import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def get_financial_news():
    """Get recent financial news headlines"""
    
    if not NEWS_API_KEY:
        print("❌ No NEWS_API_KEY in .env file!")
        return []
    
    # Search for relevant financial news
    keywords = "bitcoin OR ethereum OR crypto OR stock market OR federal reserve"
    
    # Last 24 hours
    from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        params = {
            'q': keywords,
            'from': from_date,
            'sortBy': 'popularity',
            'language': 'en',
            'pageSize': 10,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if data['status'] == 'ok':
            articles = []
            
            for article in data['articles']:
                articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'url': article['url'],
                    'published': article['publishedAt']
                })
                
                print(f"✅ {article['source']['name']}: {article['title'][:60]}...")
            
            return articles
        else:
            print(f"❌ API Error: {data.get('message', 'Unknown error')}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return []

if __name__ == "__main__":
    print("Testing News Data Collection\n")
    headlines = get_financial_news()
    print(f"\n📰 Found {len(headlines)} relevant headlines")