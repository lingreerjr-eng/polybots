import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StatArb")

class StatArb:
    def __init__(self):
        # In a real bot, we'd load this from a config or database
        self.correlated_pairs = [
            # Example: ("Trump Wins", "GOP Senate") - drift tracking
            {"id_a": "TOKEN_TRUMP", "id_b": "TOKEN_GOP", "avg_spread": 0.05, "threshold": 0.02}
        ]

    def check_correlations(self, markets):
        """
        Scans for divergence in correlated markets (Trump vs GOP Senate).
        """
    def check_correlations(self, markets):
        """
        Scans for divergence in correlated markets (Bitcoin vs Ethereum).
        """
        market_a = None
        market_b = None
        
        # 1. Find the markets in the current batch
        for m in markets:
            q = m.get('question', '').lower()
            if 'bitcoin' in q and 'december' in q:
                market_a = m
            if 'ethereum' in q and 'december' in q:
                market_b = m
        
        if market_a and market_b:
            # 2. Get prices
            try:
                p_a = float(market_a.get('bestAsk', 0))
                p_b = float(market_b.get('bestAsk', 0))
                
                if p_a > 0 and p_b > 0:
                    diff = abs(p_a - p_b)
                    
                    # Log the correlation check
                    logger.info(f"[S2-StatArb] Price Check | BTC_Var({p_a}) vs ETH_Var({p_b})")
                    
                    if diff > 0.2: 
                        return [{"type": "STAT_ARB", "diff": diff, "pair": "BTC/ETH"}]
            except:
                pass
                
        return []
