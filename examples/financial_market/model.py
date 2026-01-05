import os
import random

import mesa
from openai import OpenAI


class FinancialLLM:
    """
    A real connection to an LLM (OpenAI) to perform sentiment analysis.
    """

    def __init__(self):
        # This will look for the OPENAI_API_KEY environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is missing. Please set it before running."
            )

        self.client = OpenAI(api_key=api_key)

    def get_decision(self, news_headline):
        try:
            prompt = (
                f"You are a financial trading bot. Analyze this news headline: '{news_headline}'. "
                f"Decide if you should BUY, SELL, or HOLD. "
                f"Reply with exactly one word: BUY, SELL, or HOLD."
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Low cost model for examples
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise financial trading assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,  # Low temperature for consistent answers
                max_tokens=10,
            )

            decision = response.choices[0].message.content.strip().upper()

            # Safety fallback if model outputs extra text
            if "BUY" in decision:
                return "BUY"
            if "SELL" in decision:
                return "SELL"
            return "HOLD"

        except Exception as e:
            print(f"LLM Error: {e}")
            return "HOLD"


class TraderAgent(mesa.Agent):
    def __init__(self, unique_id, model, llm_client):
        super().__init__(model)
        self.unique_id = unique_id
        self.cash = 1000
        self.stocks = 10
        self.llm = llm_client  # Shared LLM client to save memory

    @property
    def wealth(self):
        return self.cash + (self.stocks * self.model.current_price)

    def step(self):
        news = self.model.current_news

        # Real LLM Call
        decision = self.llm.get_decision(news)

        price = self.model.current_price
        if decision == "BUY" and self.cash >= price:
            self.cash -= price
            self.stocks += 1
            self.model.buy_orders += 1
        elif decision == "SELL" and self.stocks > 0:
            self.cash += price
            self.stocks -= 1
            self.model.sell_orders += 1


class FinancialMarket(mesa.Model):
    def __init__(self, n=5):
        super().__init__()
        self.num_agents = n
        self.current_price = 100.0
        self.buy_orders = 0
        self.sell_orders = 0
        self.current_news = ""

        # Initialize one shared LLM client to prevent recreating it 5 times
        try:
            self.llm_client = FinancialLLM()
        except ValueError as e:
            print(f"Setup Error: {e}")
            self.running = False
            # Create a dummy client if real one fails, effectively stopping simulation logic but allowing init
            # Or better, just let it fail so user knows key is missing?
            # The prompt says "running = False" and return, so we rely on that.
            self.llm_client = None
            return

        self.news_feed = [
            "Tech sector reports record breaking profits!",
            "Uncertainty looms as inflation hits new highs.",
            "Housing market crash predicted by experts.",
            "New trade deal promises economic growth.",
            "Market remains stable with no major changes.",
        ]

        for i in range(self.num_agents):
            TraderAgent(i, self, self.llm_client)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Price": "current_price",
                "News": "current_news",
                "Buys": "buy_orders",
                "Sells": "sell_orders",
            },
            agent_reporters={"Wealth": "wealth"},
        )

    def step(self):
        if not self.running or not self.llm_client:
            return

        self.buy_orders = 0
        self.sell_orders = 0
        self.current_news = random.choice(self.news_feed)

        # Shuffle_do is the efficient way to run steps in Mesa 3.0
        self.agents.shuffle_do("step")

        net_demand = self.buy_orders - self.sell_orders
        self.current_price = self.current_price * (1 + (net_demand * 0.01))
        self.datacollector.collect(self)
