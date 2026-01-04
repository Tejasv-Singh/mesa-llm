import random

import mesa


class MockFinancialLLM:
    """
    Simulates an LLM for testing purposes.
    In a real scenario, you would replace this with an API call to OpenAI/Anthropic.
    """

    def get_decision(self, news_headline):
        # 1. Simulating the 'Prompt' analysis
        # We look for keywords to decide sentiment
        headline_lower = news_headline.lower()

        # 2. Simulating the 'Generation'
        if any(
            word in headline_lower
            for word in ["profit", "record", "deal", "growth", "boom"]
        ):
            return "BUY"
        elif any(
            word in headline_lower
            for word in ["crash", "loss", "inflation", "disaster", "crisis"]
        ):
            return "SELL"
        else:
            return "HOLD"


class TraderAgent(mesa.Agent):
    """
    An agent that trades stocks based on news sentiment.
    """

    def __init__(self, unique_id, model):
        super().__init__(model)
        self.unique_id = unique_id
        self.cash = 1000  # Initial Cash ($)
        self.stocks = 10  # Initial Stock Count
        self.wealth = self.calculate_wealth()
        # Give every agent access to the "LLM"
        self.llm = MockFinancialLLM()

    def calculate_wealth(self):
        return self.cash + (self.stocks * self.model.current_price)

    def step(self):
        # 1. PERCEIVE: Read the current news from the environment
        news = self.model.current_news

        # 2. REASON: Ask the "LLM" what to do based on the news
        # In a real app: response = self.llm.generate(f"Analyze this news: {news}")
        decision = self.llm.get_decision(news)

        # 3. ACT: Execute the trade
        price = self.model.current_price

        if decision == "BUY" and self.cash >= price:
            self.cash -= price
            self.stocks += 1
            self.model.buy_orders += 1

        elif decision == "SELL" and self.stocks > 0:
            self.cash += price
            self.stocks -= 1
            self.model.sell_orders += 1

        # Update wealth for data collection
        self.wealth = self.calculate_wealth()


class FinancialMarket(mesa.Model):
    """
    The environment that holds the agents, the stock price, and the news feed.
    """

    def __init__(self, n=5):
        super().__init__()
        self.num_agents = n
        # self.schedule = mesa.time.RandomActivation(self) # Removed in Mesa 3.0
        self.current_price = 100.0

        # Market tracking variables
        self.buy_orders = 0
        self.sell_orders = 0
        self.current_news = ""

        # A simulated news feed
        self.news_feed = [
            "Tech sector reports record breaking profits!",
            "Uncertainty looms as inflation hits new highs.",
            "Housing market crash predicted by experts.",
            "New trade deal promises economic growth.",
            "Market remains stable with no major changes.",
        ]

        # Create Agents
        for i in range(self.num_agents):
            TraderAgent(i, self)
            # self.schedule.add(agent) # Automatically registered in Mesa 3.0

        # Data Collector to track the simulation
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
        # Reset daily counters
        self.buy_orders = 0
        self.sell_orders = 0

        # 1. Update Environment (New Day, New News)
        self.current_news = random.choice(self.news_feed)

        # 2. Run Agents
        self.agents.shuffle_do("step")

        # 3. Market Mechanics (Price Adjustment)
        # Simple Logic: More buys = Price Up, More Sells = Price Down
        net_demand = self.buy_orders - self.sell_orders
        self.current_price = self.current_price * (1 + (net_demand * 0.01))

        # Collect Data
        self.datacollector.collect(self)
