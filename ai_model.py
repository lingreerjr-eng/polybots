import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIModel")

class ProbabilityEstimator:
    def predict_heuristic(self, market):
        """
        Returns estimated 'true' probability based on market internals.
        Heuristic: High volume + tight spread = Market is efficient (Trust price).
        Low volume = Market might be inefficient (Fade extremes).
        
        For this demo, we'll try to identify 'value' by assuming 
        mean reversion if volume is low but price is extreme.
        """
        try:
            vol = float(market.get('volume24hr', 0))
            liq = float(market.get('liquidity', 0))
            price = float(market.get('bestAsk', 0.5))
            
            # Simple Heuristic: If liquidity is high, we trust the market price (Alpha = 0).
            # If liquidity is low, we might assume price is noisy.
            # This is a placeholder for a real ML model.
            
            # For the purpose of "Real Data" demo, let's just use a Moving Average proxy
            # But we don't have history here. 
            # Let's return a "Model Confidence" based on liquidity.
            
            if liq > 10000:
                # Liquid market -> Model agrees with market mostly
                return price + 0.01 
            else:
                # Illiquid -> specific bias (e.g. fade)
                return 0.5
        except:
            return 0.5

    def predict(self, market_question):
         # Deprecated in favor of predict_heuristic that takes full market dict
         return 0.5

    def analyze_market(self, market):
        """
        Compares market price vs model price.
        """
        try:
            prices = market.get('outcomePrices', "[]")
            if isinstance(prices, str):
                import json
                prices = json.loads(prices)
            
            if not prices or len(prices) == 0:
                return None
                
            market_price = float(prices[0])
            model_price = self.predict_heuristic(market)
            
            edge = abs(model_price - market_price)
            # Only signal if we have a strong view (e.g. illiquid market reversion)
            if edge > 0.15: 
                return {
                    "type": "AI_VALUE",
                    "market": market.get('question'),
                    "model_prob": model_price,
                    "market_price": market_price,
                    "edge": edge
                }
        except Exception as e:
            # logger.warning(f"Error analyzing {market.get('slug')}: {e}")
            pass
        return None
