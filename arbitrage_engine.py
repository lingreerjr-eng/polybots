import requests
import logging
from config import CLOB_API_URL, ARB_THRESHOLD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArbitrageEngine")

class ArbitrageEngine:
    def __init__(self):
        self.session = requests.Session()

    def check_opportunity(self, market):
        """
        Checks for arbitrage opportunity in a binary market.
        market: dict containing 'clobTokenIds' and 'question'
        """
        # Strategy 1 Restriction: Only target 15-min/Bitcoin windows
        if "Bitcoin" not in market.get('question', ''):
            return None

        token_yes = market['clobTokenIds'][0]
        token_no = market['clobTokenIds'][1]
        
        # We need to fetch order books for both tokens to find the Lowest ASK (Buy price)
        # Actually, for YES/NO markets, they are often linked in the same orderbook structure 
        # but CLOB API usually exposes them via token_id.
        
        price_yes = self._get_best_ask(token_yes)
        price_no = self._get_best_ask(token_no)
        
        if price_yes is None or price_no is None:
            return None

        total_cost = price_yes + price_no
        
        if total_cost < ARB_THRESHOLD:
            return {
                "market_id": market.get('conditionId'), # or id
                "question": market.get('question'),
                "price_yes": price_yes,
                "price_no": price_no,
                "total_cost": total_cost,
                "profit_potential": 1.0 - total_cost,
                "roi": (1.0 - total_cost) / total_cost
            }
        
        return None

    def _get_best_ask(self, token_id):
        """
        Fetches the lowest ASK price for a token.
        """
        endpoint = f"{CLOB_API_URL}/book"
        params = {"token_id": token_id}
        
        try:
            response = self.session.get(endpoint, params=params, timeout=2)
            if response.status_code != 200:
                return None
                
            data = response.json()
            # Structure: { "asks": [ {"price": "0.55", "size": "100"}, ... ], "bids": ... }
            asks = data.get('asks', [])
            
            if not asks:
                return None
            
            # Asks are usually sorted by price ascending, but let's be safe
            # They come as strings.
            best_ask_price = float(asks[0]['price'])
            return best_ask_price
            
        except Exception as e:
            # logger.warning(f"Failed to fetch book for {token_id}: {e}")
            return None

if __name__ == "__main__":
    # Test with a dummy token ID if known, or just run main
    pass
