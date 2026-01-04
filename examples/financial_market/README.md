# LLM-Driven Financial Market Simulation

This project demonstrates an Agent-Based Model (ABM) where trading agents make decisions based on **natural language news headlines** rather than traditional mathematical indicators. It uses the [Mesa framework](https://github.com/projectmesa/mesa) for the simulation engine and a mocked Large Language Model (LLM) to simulate cognitive decision-making.

## 🚀 Key Features

*   **Cognitive Agents**: Agents "read" news and interpret sentiment to make trading decisions.
*   **Natural Language Processing**: Uses a keyword-based mock LLM to classify news as Bullish (Buy), Bearish (Sell), or Neutral (Hold).
*   **Dynamic Market**: Stock price fluctuates based on real-time supply and demand from agent actions.
*   **Extensible Design**: The "Mock LLM" is designed to be easily swapped with real APIs like OpenAI GPT-4 or Anthropic Claude.

## 📂 Project Structure

*   **`model.py`**: The core logic. Defines:
    *   `MockFinancialLLM`: Simulates an AI analyst perceiving market sentiment.
    *   `TraderAgent`: The economic actor that perceives news, consults the LLM, and executes trades.
    *   `FinancialMarket`: The environment managing the order book, price updates, and news generation.
*   **`run.py`**: A CLI runner that executes the simulation step-by-step and prints a tabular report of the market state.
*   **`requirements.txt`**: Project dependencies.

## 🧠 Simulation Logic

1.  **News Generation**: Each step (day), the market emits a random news headline (e.g., *"Tech sector reports record breaking profits!"*).
2.  **Perception (Agent Layer)**:
    *   Agents receive the headline.
    *   They pass it to their internal `llm` model.
3.  **Reasoning (Cognitive Layer)**:
    *   The `MockFinancialLLM` analyzes keywords (e.g., "profit" -> BUY, "crash" -> SELL).
    *   It returns a decision: **BUY**, **SELL**, or **HOLD**.
4.  **Action (Market Layer)**:
    *   **BUY**: If the agent has cash, they buy stock.
    *   **SELL**: If the agent has stock, they sell for cash.
5.  **Market Reaction**:
    *   Aggregated Buy/Sell orders shift the stock price up or down (1% shift per net order).

## 🛠️ Installation & Usage

### Prerequisites
*   Python 3.10+
*   pip

### Steps

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Simulation**
    ```bash
    python run.py
    ```

### Example Output

```text
Step  | Price ($)  | Orders (B/S)    | News Headline
-------------------------------------------------------------------------------------
0     | 100.05     | 5 / 0           | Tech sector reports record breaking profits!
1     | 99.55      | 0 / 5           | Housing market crash predicted by experts.
2     | 99.55      | 0 / 0           | Market remains stable with no major changes.
...
```

## 🔌 How to Connect a Real LLM

To upgrade this simulation with real AI, modify `MockFinancialLLM` in `model.py`:

```python
# pseudocode example
import openai

class RealFinancialLLM:
    def get_decision(self, news_headline):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst. Respond only with BUY, SELL, or HOLD."},
                {"role": "user", "content": f"Analyze this news: {news_headline}"}
            ]
        )
        return response.choices[0].message.content.strip()
```
