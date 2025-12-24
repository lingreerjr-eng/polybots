import os
from dotenv import load_dotenv

load_dotenv()

# API Endpoints
GAMMA_API_URL = "https://gamma-api.polymarket.com"
CLOB_API_URL = "https://clob.polymarket.com"

# Strategy Parameters
ARB_THRESHOLD = 0.99  # Combined price check
MIN_LIQUIDITY = 1000  # Minimum liquidity to consider a market
POLL_INTERVAL = 1.0   # Seconds between polls

# Credentials (load from env)
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
API_KEY = os.getenv("CLOB_API_KEY")
API_SECRET = os.getenv("CLOB_API_SECRET")
API_PASSPHRASE = os.getenv("CLOB_API_PASSPHRASE")
FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS")

# Wallet / Chain Config
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" # USDC.e on Polygon
PROXY_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045" # Polymarket CTF Exchange Proxy (check docs if changed)

# Market Filtering
TARGET_TAGS = ["Crypto", "Politics"]
