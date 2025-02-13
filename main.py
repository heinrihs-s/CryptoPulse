import requests
import numpy as np
import openai
from datetime import datetime, timedelta

# Set your API keys
openai.api_key = "YOUR_OPENAI_API_KEY"
GLASSNODE_API_KEY = "YOUR_GLASSNODE_API_KEY"

###############################
# Fetch and Process CoinGecko Data
###############################

def fetch_crypto_data(coin_id="bitcoin", vs_currency="usd", days=7):
    """
    Fetch historical market data for a cryptocurrency from CoinGecko.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data from CoinGecko: {response.status_code} - {response.text}")

def process_crypto_data(data):
    """
    Process CoinGecko data to extract key metrics.
    """
    prices = data.get("prices", [])
    if not prices:
        raise Exception("No price data available from CoinGecko.")

    # Extract timestamps and price values
    timestamps = [entry[0] for entry in prices]
    price_values = [entry[1] for entry in prices]

    # Convert timestamps (in ms) to human-readable dates
    dates = [datetime.fromtimestamp(ts / 1000.0).strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps]

    start_price = price_values[0]
    end_price = price_values[-1]
    average_price = np.mean(price_values)
    volatility = np.std(price_values)
    highest_price = np.max(price_values)
    lowest_price = np.min(price_values)
    percentage_change = ((end_price - start_price) / start_price) * 100

    return {
        "start_date": dates[0],
        "end_date": dates[-1],
        "start_price": start_price,
        "end_price": end_price,
        "average_price": average_price,
        "volatility": volatility,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "percentage_change": percentage_change
    }

###############################
# Fetch and Process Glassnode Data
###############################

def fetch_glassnode_data(asset="BTC", metric="addresses/active_count", start_timestamp=None, end_timestamp=None):
    """
    Fetch on-chain data from Glassnode.
    
    For this example, we're using the 'addresses/active_count' metric.
    """
    url = f"https://api.glassnode.com/v1/metrics/{metric}"
    params = {
        "api_key": GLASSNODE_API_KEY,
        "asset": asset,
        "start": start_timestamp,
        "end": end_timestamp
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching Glassnode data: {response.status_code} - {response.text}")

def process_glassnode_data(data):
    """
    Process the Glassnode data to calculate key on-chain metrics.
    
    Assumes data is a list of dicts with:
      - 't': timestamp (in seconds)
      - 'v': metric value (active addresses count)
    """
    if not data:
        raise Exception("No on-chain data available from Glassnode.")

    # Extract timestamps and values
    timestamps = [entry["t"] for entry in data]
    values = [entry["v"] for entry in data]

    # Convert timestamps to human-readable dates (for the first and last entry)
    start_date = datetime.fromtimestamp(timestamps[0]).strftime("%Y-%m-%d %H:%M:%S")
    end_date = datetime.fromtimestamp(timestamps[-1]).strftime("%Y-%m-%d %H:%M:%S")

    average_active = np.mean(values)
    highest_active = np.max(values)
    lowest_active = np.min(values)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "average_active_addresses": average_active,
        "highest_active_addresses": highest_active,
        "lowest_active_addresses": lowest_active
    }

###############################
# LLM Prompt Generation & Analysis
###############################

def generate_prompt(coin_id, market_data, onchain_data):
    """
    Generate a prompt for the LLM that includes both market and on-chain metrics.
    """
    prompt = (
        f"Analyze the current state of {coin_id} by considering both market and on-chain data.\n\n"
        f"**Market Data (CoinGecko):**\n"
        f"- **Start Date:** {market_data['start_date']} with price ${market_data['start_price']:.2f}\n"
        f"- **End Date:** {market_data['end_date']} with price ${market_data['end_price']:.2f}\n"
        f"- **Average Price:** ${market_data['average_price']:.2f}\n"
        f"- **Volatility (Std Dev):** ${market_data['volatility']:.2f}\n"
        f"- **Highest Price:** ${market_data['highest_price']:.2f}\n"
        f"- **Lowest Price:** ${market_data['lowest_price']:.2f}\n"
        f"- **Percentage Change:** {market_data['percentage_change']:.2f}%\n\n"
        f"**On-Chain Data (Glassnode - Active Addresses):**\n"
        f"- **Observation Period:** {onchain_data['start_date']} to {onchain_data['end_date']}\n"
        f"- **Average Active Addresses:** {onchain_data['average_active_addresses']:.0f}\n"
        f"- **Highest Active Addresses:** {onchain_data['highest_active_addresses']:.0f}\n"
        f"- **Lowest Active Addresses:** {onchain_data['lowest_active_addresses']:.0f}\n\n"
        "Based on this data, please provide a detailed market analysis. "
        "Discuss trends, possible correlations between price movements and on-chain activity, "
        "and any potential signals or risks for investors."
    )
    return prompt

def get_llm_analysis(prompt):
    """
    Use OpenAI's ChatCompletion API to generate an analysis based on the prompt.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a seasoned cryptocurrency market and on-chain analytics expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM analysis failed: {e}"

###############################
# Main Function
###############################

def main():
    coin_id = "bitcoin"      # CoinGecko coin id (e.g., "bitcoin")
    asset = "BTC"            # Glassnode asset symbol (e.g., "BTC")
    days = 7                 # Number of days for historical data

    # Calculate time windows
    # For CoinGecko, the API handles 'days' automatically.
    # For Glassnode, compute Unix timestamps (in seconds).
    end_timestamp = int(datetime.now().timestamp())
    start_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())

    try:
        # Fetch and process market data
        raw_market_data = fetch_crypto_data(coin_id=coin_id, days=days)
        market_data = process_crypto_data(raw_market_data)
        
        # Fetch and process on-chain data from Glassnode
        raw_onchain_data = fetch_glassnode_data(asset=asset, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        onchain_data = process_glassnode_data(raw_onchain_data)
        
        # Generate combined prompt
        prompt = generate_prompt(coin_id, market_data, onchain_data)
        print("=== Generated Prompt for LLM ===")
        print(prompt)
        
        # Get analysis from the LLM
        print("\n=== LLM Analysis ===")
        analysis = get_llm_analysis(prompt)
        print(analysis)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
