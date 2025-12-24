import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SpreadFarmer")

class SpreadFarmer:
    def __init__(self):
        self.min_spread = 0.02

    def scan_spreads(self, markets):
        opportunities = []
        for m in markets:
            try:
                # Gamma markets data sometimes has 'bestBid' 'bestAsk'
                bid = float(m.get('bestBid') or 0)
                ask = float(m.get('bestAsk') or 0)
                
                if bid > 0 and ask > 0:
                    spread = ask - bid
                    if spread >= self.min_spread:
                        opportunities.append({
                            "type": "SPREAD_FARM",
                            "market": m.get('question'),
                            "bid": bid,
                            "ask": ask,
                            "spread": spread
                        })
                        logger.info(f"[S4] Spread {spread:.3f} on {m.get('slug')}")
            except:
                continue
        return opportunities
