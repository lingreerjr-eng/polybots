import logging
import os
from web3 import Web3

try:
    from py_clob_client.client import ClobClient
except ImportError:
    ClobClient = None

from config import (
    PRIVATE_KEY, API_KEY, API_SECRET, API_PASSPHRASE, 
    POLYGON_RPC_URL, USDC_ADDRESS, PROXY_ADDRESS, FUNDER_ADDRESS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Execution")

class OrderExecutor:
    def __init__(self):
        self.ready = False
        if not all([PRIVATE_KEY, API_KEY, API_SECRET, API_PASSPHRASE, FUNDER_ADDRESS]):
            logger.warning("Missing credentials/wallet info. Execution mode: SIMULATION")
            return

        try:
            # 1. Setup Web3
            self.w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
            self.account = self.w3.eth.account.from_key(PRIVATE_KEY)
            self.chain_id = 137 # Polygon Mainnet

            # 2. Setup CLOB Client
            if ClobClient:
                self.client = ClobClient(
                    host="https://clob.polymarket.com",
                    key=PRIVATE_KEY,
                    chain_id=self.chain_id,
                    creds=None 
                )
                self.client.set_api_creds(
                    api_key=API_KEY,
                    api_secret=API_SECRET,
                    api_passphrase=API_PASSPHRASE
                )
            else:
                self.client = None
                logger.warning("py-clob-client not found. Trading will be SIMULATED.")
            
            logger.info(f"Executor initialized for {FUNDER_ADDRESS}")
            self.ready = True
        except Exception as e:
            logger.error(f"Failed to init Executor: {e}")

    def check_allowance(self):
        """
        Checks if USDC allowance is sufficient for the Proxy.
        """
        # ready is True if Web3 init passed, even if CLOB failed.
        if not self.ready: return False
        
        usdc_abi = [
            {"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"type":"function"},
            {"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"}
        ]
        
        contract = self.w3.eth.contract(address=USDC_ADDRESS, abi=usdc_abi)
        allowance = contract.functions.allowance(FUNDER_ADDRESS, PROXY_ADDRESS).call()
        
        logger.info(f"Current USDC Allowance: {allowance / 1e6}")
        
        if allowance < 1000 * 1e6: # Less than $1000
             logger.warning("Low allowance. Please approve USDC for Polymarket Proxy.")
             return False
        return True

    def place_order(self, token_id, price, size, side="BUY"):
        """
        Places a limit order. 
        """
        if not self.ready or self.client is None:
            logger.info(f"[SIMULATION] Placing {side} Order: Token={token_id}, Price={price}, Size={size}")
            return

        try:
            # py-clob-client handles creating and signing the order
            resp = self.client.create_and_post_order(
                token_id=token_id,
                price=price,
                side=side.upper(),
                size=size,
                order_type="GTC"
            )
            logger.info(f"Order Placed! ID: {resp.get('orderID')}")
            return resp
        except Exception as e:
            logger.error(f"Order Failed: {e}")
            return None
