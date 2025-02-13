# CryptoPulse: AI-Driven Market & On-Chain Analytics

CryptoPulse is an innovative tool that combines real-time cryptocurrency market data with on-chain analytics and advanced AI-driven insights. By integrating data from CoinGecko and Glassnode, then processing it with powerful Python analytics and OpenAI's LLM models, CryptoPulse provides investors and enthusiasts with comprehensive market analysis, highlighting trends, correlations, and potential risks.

## Features

- **Market Data Integration**: Retrieves historical cryptocurrency prices from CoinGecko
- **On-Chain Metrics**: Fetches active address data from Glassnode to gauge blockchain activity
- **Data Processing**: Calculates key metrics including average price, volatility, percentage change, highest & lowest prices
- **AI-Driven Analysis**: Generates in-depth market commentary using OpenAI's GPT-3.5 Turbo
- **Customizable Parameters**: Easily adjust coin selections, timeframes, and metric settings to suit your needs

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/heinrihs-s/CryptoPulse.git
cd CryptoPulse
```

### 2. Install Dependencies

Ensure you have Python 3.7 or later installed. Then, install the required packages:

```bash
pip install requests numpy openai
```

## Configuration

Before running the project, you need to configure your API keys:

- **OpenAI API Key**: Replace `"YOUR_OPENAI_API_KEY"` in the script with your actual OpenAI API key
- **Glassnode API Key**: Replace `"YOUR_GLASSNODE_API_KEY"` in the script with your actual Glassnode API key

## Usage

Run the main script to fetch data, process metrics, generate a prompt, and receive an AI-powered market analysis:

```bash
python main.py
```

Upon execution, the script will:

1. Fetch historical market data from CoinGecko
2. Retrieve on-chain data (active addresses) from Glassnode
3. Process and analyze the data to extract meaningful metrics
4. Generate a detailed prompt that is sent to OpenAI's GPT-3.5 Turbo
5. Display the generated prompt and the AI's market analysis in your terminal

## How It Works

### 1. Data Fetching
- **CoinGecko**: Retrieves price history over a specified number of days
- **Glassnode**: Acquires on-chain metrics like active addresses within a defined time window

### 2. Data Processing
- Extracts timestamps, computes average price, volatility, highest/lowest values, and calculates percentage changes
- Processes on-chain data to determine average, highest, and lowest active address counts

### 3. AI Analysis
- Combines market and on-chain data into a comprehensive prompt
- Uses OpenAI's ChatCompletion API to generate a detailed market analysis

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create a new branch** for your feature or bugfix
3. **Implement your changes**
4. **Submit a pull request** with a clear description of your modifications

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Disclaimer

This project is provided for educational and informational purposes only. The AI-generated analysis is not financial advice. Always perform your own research before making any investment decisions.


