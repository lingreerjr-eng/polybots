import requests
import json
import logging
from config import GAMMA_API_URL, TARGET_TAGS, MIN_LIQUIDITY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MarketFetcher")

class MarketFetcher:
    def __init__(self):
        self.session = requests.Session()

    def fetch_markets(self):
        """
        Fetches active markets from Gamma API.
        Returns a list of market dictionaries.
        """
        endpoint = f"{GAMMA_API_URL}/markets"
        params = {
            "active": "true",
            "closed": "false",
            "limit": 100,
            "order": "volume24hr",
            "ascending": "false"
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            markets = []
            if isinstance(data, list):
                markets = data
            elif isinstance(data, dict) and 'data' in data:
                markets = data['data']
            else:
                logger.error(f"Unexpected API response format: {type(data)}")
                return []

            filtered_markets = self._filter_markets(markets)
            return filtered_markets

        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []

    def _filter_markets(self, markets):
        valid_markets = []
        for m in markets:
            # Basic validation
            if not m.get('enableOrderBook'):
                continue
            
            # Liquidity check
            if float(m.get('liquidity', 0) or 0) < MIN_LIQUIDITY:
                continue

            # Parse clobTokenIds
            try:
                if isinstance(m.get('clobTokenIds'), str):
                    m['clobTokenIds'] = json.loads(m['clobTokenIds'])
                
                if not m['clobTokenIds'] or len(m['clobTokenIds']) != 2:
                    continue 

                valid_markets.append(m)
            except:
                continue
                
        return valid_markets

if __name__ == "__main__":
    fetcher = MarketFetcher()
    markets = fetcher.fetch_markets()
    print(f"Fetched {len(markets)} valid markets.")
