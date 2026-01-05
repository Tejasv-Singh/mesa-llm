# Financial Market Simulation (Real LLM)

This example uses **OpenAI's GPT Models** to drive agent decision-making. Agents analyze simulated news headlines and decide to trade stocks based on the sentiment.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API Key**: You must have an OpenAI API key. Set it as an environment variable:

   **Mac/Linux:**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

   **Windows (Powershell):**
   ```powershell
   $env:OPENAI_API_KEY="sk-..."
   ```

## Running the Model

```bash
python run.py
```
