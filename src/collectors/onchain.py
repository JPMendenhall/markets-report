import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
# V2 API base URL
BASE_URL = "https://api.etherscan.io/v2/api"

def get_eth_price():
    """Get current ETH price in USD using CoinGecko as backup"""
    try:
        # Use CoinGecko instead since it's more reliable
        from pycoingecko import CoinGeckoAPI
        cg = CoinGeckoAPI()
        data = cg.get_price(ids='ethereum', vs_currencies='usd')
        return float(data['ethereum']['usd'])
    except Exception as e:
        print(f"⚠️  Could not fetch ETH price: {e}")
        return 0

def get_gas_price():
    """Get current gas price - V2 endpoint"""
    try:
        params = {
            'chainid': 1,  # Ethereum mainnet
            'module': 'gastracker',
            'action': 'gasoracle',
            'apikey': ETHERSCAN_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if data['status'] == '1' and 'result' in data:
            return {
                'safe': data['result']['SafeGasPrice'],
                'propose': data['result']['ProposeGasPrice'],
                'fast': data['result']['FastGasPrice']
            }
        
    except Exception as e:
        print(f"⚠️  Error fetching gas price: {e}")
    
    return None

def get_block_info():
    """Get latest block info - V2 endpoint"""
    try:
        params = {
            'chainid': 1,
            'module': 'proxy',
            'action': 'eth_blockNumber',
            'apikey': ETHERSCAN_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if 'result' in data:
            block_number = int(data['result'], 16)  # Convert hex to int
            print(f"✅ Latest block: {block_number:,}")
            return block_number
        
    except Exception as e:
        print(f"⚠️  Error fetching block: {e}")
    
    return None

def get_onchain_summary():
    """Get summary of on-chain activity"""
    
    print("Fetching on-chain data...\n")
    
    # ETH price (from CoinGecko - more reliable)
    eth_price = get_eth_price()
    print(f"💰 ETH Price: ${eth_price:,.2f}")
    
    # Gas prices
    gas = get_gas_price()
    if gas:
        print(f"⛽ Gas (Gwei): Safe={gas['safe']}, Standard={gas['propose']}, Fast={gas['fast']}")
    
    # Latest block
    block = get_block_info()
    
    return {
        'eth_price': eth_price,
        'gas_prices': gas,
        'latest_block': block,
        'timestamp': datetime.now()
    }

if __name__ == "__main__":
    print("Testing On-Chain Data Collection\n")
    
    if not ETHERSCAN_API_KEY:
        print("❌ No ETHERSCAN_API_KEY in .env file!")
        exit(1)
    
    print(f"Using Etherscan API V2\n")
    
    summary = get_onchain_summary()
    
    print(f"\n✅ On-chain data collected successfully")