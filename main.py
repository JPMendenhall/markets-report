import os
from datetime import datetime
from collectors.tradfi import get_market_snapshot as get_tradfi
from collectors.crypto import get_crypto_snapshot as get_crypto
from collectors.onchain import get_onchain_summary as get_onchain
from collectors.news import get_financial_news as get_news
from analyzer import analyze_markets
from reporter import generate_html_report


# Create reports directory if it doesn't exist
os.makedirs("reports", exist_ok=True)

def collect_all_data():
    """Run all data collectors"""
    
    print("="*70)
    print("COLLECTING MARKET DATA")
    print("="*70)
    
    print("\n📊 Traditional Markets...")
    tradfi = get_tradfi()
    
    print("\n💰 Crypto Markets...")
    crypto = get_crypto()
    
    print("\n⛓️  On-Chain Data...")
    onchain = get_onchain()
    
    print("\n📰 News Headlines...")
    news = get_news()
    
    return tradfi, crypto, onchain, news

def generate_daily_report():
    """Main function - collect data and generate report"""
    
    print(f"\n🚀 MARKETS REPORT - {datetime.now().strftime('%B %d, %Y')}")
    print("="*70)
    
    # Collect all data
    tradfi, crypto, onchain, news = collect_all_data()
    
    # Analyze with AI
    print("\n" + "="*70)
    print("ANALYZING DATA WITH AI")
    print("="*70 + "\n")
    
    analysis = analyze_markets(tradfi, crypto, onchain, news)
    
    if analysis:
        print("\n" + "="*70)
        print("TODAY'S MARKET ANALYSIS")
        print("="*70)
        print(analysis)
        
        # Package data
        report_data = {
            'tradfi': tradfi,
            'crypto': crypto,
            'onchain': onchain,
            'news': news,
            'analysis': analysis,
            'timestamp': datetime.now()
        }
        
        # Generate HTML report
        print("\n" + "="*70)
        print("GENERATING HTML REPORT")
        print("="*70 + "\n")
        
        filepath = generate_html_report(report_data)
        
        print(f"\n✅ Report complete! Open: {filepath}")
        
        return report_data
    else:
        print("❌ Failed to generate analysis")
        return None

if __name__ == "__main__":
    report = generate_daily_report()