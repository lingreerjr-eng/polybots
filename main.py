import time
import logging
from market_fetcher import MarketFetcher
from arbitrage_engine import ArbitrageEngine
from stat_arb import StatArb
from ai_model import ProbabilityEstimator
from market_maker import SpreadFarmer
from copy_trader import CopyTrader
from execution import OrderExecutor
from config import POLL_INTERVAL

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Main")

def main():
    logger.info("Starting Polymarket Arbitrage Bot (All Strategies)")
    
    fetcher = MarketFetcher()
    
    # Initialize Strategies
    strat1_arb = ArbitrageEngine()
    strat2_stat = StatArb()
    strat3_ai = ProbabilityEstimator()
    strat4_mm = SpreadFarmer()
    strat5_copy = CopyTrader()
    
    # Initialize Executor
    executor = OrderExecutor()
    if executor.ready:
        executor.check_allowance()
    
    while True:
        try:
            # 1. Fetch Markets
            logger.info("Fetching markets...")
            markets = fetcher.fetch_markets()
            logger.info(f"Scanning {len(markets)} active markets...")
            
            # 2. Strategy 1: Simple Arb
            opportunities = []
            for market in markets:
                # S1: Simple Arb
                opp = strat1_arb.check_opportunity(market)
                if opp:
                    logger.info(f"[S1] ARB FOUND: {opp['question']} | Profit: ${opp['profit_potential']:.3f}")
                    # Attempt Execution (Example: Buy $10 worth)
                    # Note: We need token IDs from the market object.
                    # This is a basic example; real execution needs precise sizing.
                    # executor.place_order(token_id=..., price=..., size=10)
                
                # S3: AI Model
                ai_opp = strat3_ai.analyze_market(market)
                if ai_opp:
                    logger.info(f"[S3] AI VALUE: {ai_opp['market']} | Edge: {ai_opp['edge']:.2f}")

            # S4: Spread Farming
            spread_opps = strat4_mm.scan_spreads(markets)
            if spread_opps:
                logger.info(f"[S4] Found {len(spread_opps)} spread farming candidates.")

            # S2 & S5 (Placeholder checks)
            strat2_stat.check_correlations(markets)
            strat5_copy.check_targets()
            
            logger.info("Scan complete.")
            
            # Wait for next poll
            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
