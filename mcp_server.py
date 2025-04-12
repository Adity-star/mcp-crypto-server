import os
import httpx
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Create our MCP server with a descriptive name
mcp = FastMCP("crypto_price_tracker")

@mcp.tool()
async def get_crypto_market_info(crypto_ids: str, currency: str = "USD") -> str:
    """
    Get market information for one or more cryptocurrencies using Alpha Vantage.
    
    Parameters:
    - crypto_ids: Comma-separated list of cryptocurrency symbols (e.g., 'BTC,ETH')
    - currency: The fiat currency to compare against (default: 'USD')
    
    Returns:
    - Current exchange rates for each cryptocurrency.
    """
    symbols = [sym.strip().upper() for sym in crypto_ids.split(",")]
    currency = currency.upper()
    result = ""

    try:
        async with httpx.AsyncClient() as client:
            for symbol in symbols:
                url = (
                    f"{ALPHA_VANTAGE_BASE_URL}?function=CURRENCY_EXCHANGE_RATE"
                    f"&from_currency={symbol}&to_currency={currency}&apikey={ALPHA_VANTAGE_API_KEY}"
                )
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                rate_info = data.get("Realtime Currency Exchange Rate", {})
                if not rate_info:
                    result += f"❌ Could not retrieve data for {symbol}{currency}.\n\n"
                    continue

                exchange_rate = rate_info.get("5. Exchange Rate", "Unknown")
                last_refreshed = rate_info.get("6. Last Refreshed", "Unknown")

                result += f"{symbol}/{currency}:\n"
                result += f"Current price: {exchange_rate} {currency}\n"
                result += f"Last updated: {last_refreshed}\n\n"

        return result.strip()

    except Exception as e:
        return f"Error fetching data from Alpha Vantage: {str(e)}"


# Run the MCP server
if __name__ == "__main__":
    mcp.run()
