from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_crypto_snapshot():
    """Get current crypto market data"""
    
    # Top coins to track
    coins = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot']
    
    results = {}
    
    try:
        # Get price data with 24h change
        data = cg.get_price(
            ids=coins,
            vs_currencies='usd',
            include_24hr_change=True,
            include_market_cap=True,
            include_24hr_vol=True
        )
        
        for coin in coins:
            if coin in data:
                price = data[coin]['usd']
                change = data[coin].get('usd_24h_change', 0)
                
                results[coin] = {
                    'price': round(price, 2),
                    'change_24h': round(change, 2),
                    'market_cap': data[coin].get('usd_market_cap', 0),
                    'volume_24h': data[coin].get('usd_24h_vol', 0),
                    'direction': 'up' if change > 0 else 'down'
                }
                
                print(f"✅ {coin.title()}: ${price:,.2f} ({change:+.2f}%)")
        
    except Exception as e:
        print(f"❌ Error fetching crypto prices: {e}")
        return {}
    
    # Get global market data (separate try/catch)
    try:
        global_data = cg.get_global()
        
        if 'data' in global_data:
            total_mcap = global_data['data']['total_market_cap']['usd']
            btc_dominance = global_data['data']['market_cap_percentage']['btc']
            
            print(f"\n📊 Total Market Cap: ${total_mcap/1e12:.2f}T")
            print(f"📊 BTC Dominance: {btc_dominance:.1f}%")
            
            results['_global'] = {
                'total_market_cap': total_mcap,
                'btc_dominance': btc_dominance
            }
    except Exception as e:
        print(f"⚠️  Could not fetch global data (non-critical): {e}")
    
    return results

if __name__ == "__main__":
    print("Testing Crypto Data Collection\n")
    snapshot = get_crypto_snapshot()
    print(f"\n✅ Collected {len([k for k in snapshot.keys() if k != '_global'])} coins")