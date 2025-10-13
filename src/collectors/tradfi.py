import yfinance as yf
from datetime import datetime

def get_market_snapshot():
    """Get current state of traditional markets"""
    
    tickers = {
        'S&P 500': '^GSPC',
        'Nasdaq': '^IXIC',
        'Dow Jones': '^DJI',
        'Gold': 'GC=F',
        'VIX': '^VIX',
        '10Y Treasury': '^TNX',
        'Dollar Index': 'DX-Y.NYB'
    }
    
    data = {}
    
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='2d')
            
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change_pct = ((current - previous) / previous) * 100
                
                data[name] = {
                    'symbol': symbol,
                    'price': round(current, 2),
                    'change': round(change_pct, 2),
                    'direction': 'up' if change_pct > 0 else 'down'
                }
                
                print(f"✅ {name}: ${current:.2f} ({change_pct:+.2f}%)")
            
        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")
    
    return data

if __name__ == "__main__":
    print("Testing TradFi Data Collection\n")
    snapshot = get_market_snapshot()
    print(f"\n📊 Collected {len(snapshot)} data points")