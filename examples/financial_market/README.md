# Financial Market Simulation

A multi-agent simulation where **TraderAgents** utilize the **Mesa-LLM `ModuleLLM`** to analyze news sentiment and make trading decisions.

## Description
This model demonstrates the integration of Large Language Models (LLMs) into standard Mesa agent lifecycles.
* **Agents:** Traders who hold Cash and Stock.
* **Environment:** A dynamic market with a fluctuating stock price and a randomized news feed.
* **Decision Making:** Each agent perceives the global news and uses `ModuleLLM` to act (BUY/SELL/HOLD).

## Dependencies
This example requires the following packages:
* `mesa`
* `openai`
* `mesa-llm` (This package)

## Usage
1. **Set API Key:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

2. **Run the Simulation:**
   ```bash
   python run.py
   ```

## File Structure
* **model.py:** Contains the FinancialMarket class and environment logic.
* **agents.py:** Contains the TraderAgent class and LLM integration.
* **run.py:** CLI entry point to execute the model and view results.
