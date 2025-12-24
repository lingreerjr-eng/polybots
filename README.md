# Polymarket Arbitrage Bot

A high-frequency trading bot for Polymarket implementing 5 distinct strategies using real-time market data.

## Features

- **Real-Time Data**: Polls Polymarket's Gamma API and CLOB (Central Limit Order Book).
- **Multi-Strategy**:
    1.  **Simple Arbitrage**: Exploits `YES + NO < $0.99` pricing errors (Target: 15-min Bitcoin windows).
    2.  **Statistical Arbitrage**: Tracks correlation divergence (e.g., BTC vs ETH).
    3.  **AI Probability**: Heuristic-based value estimation using Volume/Liquidity signals.
    4.  **Spread Farming**: Identifies market-making opportunities (Spread > 2%).
    5.  **Copy-Trading**: Logic to follow whale positions.

## Prerequisites

-   Python 3.10+
-   `pip` package manager

## Installation

1.  **Clone the repository** (or navigate to the directory):
    ```bash
    cd /path/to/polysim
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The bot uses environment variables for authentication. You can set these in your shell or use a `.env` file (requires `python-dotenv`).

**Required for Real Execution (Ordering):**

Create a `.env` file in the root directory:

```env
# Wallet Configuration (Your Polygon Wallet)
PRIVATE_KEY=0xYourPrivateKeyHere
FUNDER_ADDRESS=0xYourPublicAddressHere

# Polymarket CLOB API Credentials
# Get these from https://polymarket.com/settings (API Keys)
CLOB_API_KEY=p-your-api-key
CLOB_API_SECRET=your-secret
CLOB_API_PASSPHRASE=your-passphrase

# Network Config (Optional, defaults provided)
POLYGON_RPC_URL=https://polygon-rpc.com
```

**Note**: Without these keys, the bot runs in **Dry-Run / Simulation Mode**, logging opportunities without executing trades.

## Usage

### Run the Bot
To start the main event loop (scans all strategies every ~1s):

```bash
python main.py
```

**Output:**
The bot will log activities to the console:
-   `INFO`: General status (fetching markets).
-   `[S1] ARB FOUND`: Simple Arbitrage opportunities.
-   `[S2-StatArb]`: Correlation tracking logs.
-   `[S3] AI VALUE`: AI Model value picks.
-   `[S4] Spread`: Spread farming candidates.

## Testing

### Dry Run (Default)
Simply run `python main.py` without API keys.
-   **Verify**: Check that you see "Scanning X active markets" logs.
-   **simulate**: The bot will print `*** ARBITRAGE FOUND ***` when conditions are met, but will not send transactions.

### Unit Tests (Optional)
To check the logic of specific components (e.g., Arb Engine or Filters), you can run the modules directly if they have `__main__` blocks:
```bash
python market_fetcher.py  # Tests API connection and filtering
```

## Strategy Details

1.  **Simple Arb**: Filters for markets with "Bitcoin" in the title. Calculation: `Ask(Yes) + Ask(No)`.
2.  **Stat Arb**: Looks for "Bitcoin" and "Ethereum" markets expiring in "December" to compare price moves.
3.  **AI Model**: "Predicts" probability based on a heuristic:
    -   High Liquidity (>10k) -> Trust Market Price.
    -   Low Liquidity -> Fade Price (Mean Reversion).
