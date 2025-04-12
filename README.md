# 🪙 MCP Crypto Price Lookup Server using ALPACA API

This project sets up a **cryptocurrency price lookup service** powered by the [ALPACA API](https://alpaca.markets/) and built for integration with **MCP (Multi-Agent Control Protocol)**.

The server allows AI agents or clients to fetch **real-time cryptocurrency prices and market data** efficiently using Alpaca's API.

---

## 📦 Step 1: Set Up the Environment with `uv`

We'll use [uv](https://astral.sh/blog/uv/) — a fast, modern Python package manager — to create and manage the project environment.

### 🛠️ Installation & Setup

Run these commands **in your terminal** (not in Jupyter):

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh 

# Create and navigate to your project directory
mkdir mcp-crypto-server
cd mcp-crypto-server

# Initialize a new project
uv init

# Create and activate the virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
uv add "mcp[cli]" httpx
```

## Step 2: Running the MCP Server
Once the environment is set up, we're ready to build and run our crypto price lookup tool.
Copy the server script from the scripts folder:

```bash
cp ../mcp_server.py .

Start the MCP server:
uv run mcp_server.py
```
💡 Check out [mcp_server.py]( https://github.com/Adity-star/mcp-crypto-server/blob/main/mcp_server.py) for implementation details on how the tool interfaces with the Alpaca API.


## About the Server
The MCP-compatible server includes tools that:
- Fetch real-time crypto prices (e.g., BTC/USD, ETH/USD)
- Access market data using Alpaca's REST API
- Serve AI agents with quick, formatted responses

### Step 3: Configure Your MCP Server
Add the following to your MCP config to register the server:

```bash
{
    "mcpServers": {
        "crypto-price-tracker": {
            "command": "/ABSOLUTE/PATH/TO/uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/GenAI_Agents//mcp-crypto-server",
                "run",
                "mcp_server.py"
            ]
        }
    }
}
```

🔁 Replace /ABSOLUTE/PATH/TO/... with the full paths to your uv binary and project folder.

### Step 4: Restart Claude Desktop for the changes to take effect.

### Step 5: Try ask the price of Bitcoin

- You can add your own tools to mcp_server.py
```bash
"""
This script demonstrates how to create a simple MCP server that fetches
the current price of a cryptocurrency using the CoinGecko API.
It uses the FastMCP library to create the server and handle requests.
"""
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Create our MCP server with a descriptive name
mcp = FastMCP("crypto_price_tracker")

# Now let's define our first tool - getting the current price of a cryptocurrency
@mcp.tool()
async def get_crypto_price(crypto_id: str, currency: str = "usd") -> str:
    """
    Get the current price of a cryptocurrency in a specified currency.
    
    Parameters:
    - crypto_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum')
    - currency: The currency to display the price in (default: 'usd')
    
    Returns:
    - Current price information as a formatted string
    """
    # Construct the API URL
    url = f"{COINGECKO_BASE_URL}/simple/price"
    
    # Set up the query parameters
    params = {
        "ids": crypto_id,
        "vs_currencies": currency
    }
    
    try:
        # Make the API call
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the response
            data = response.json()
            
            # Check if we got data for the requested crypto
            if crypto_id not in data:
                return f"Cryptocurrency '{crypto_id}' not found. Please check the ID and try again."
            
            # Format and return the price information
            price = data[crypto_id][currency]
            return f"The current price of {crypto_id} is {price} {currency.upper()}"
            
    except httpx.HTTPStatusError as e:
        return f"API Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error fetching price data: {str(e)}"

# You can add more tools here, following the same pattern as above

# Run the MCP server
# This will start the server and listen for incoming requests
if __name__ == "__main__":
    mcp.run()
```
