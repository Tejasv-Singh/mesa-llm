import mesa
import random
from agents import TraderAgent

class FinancialMarket(mesa.Model):
    def __init__(self, n=5):
        super().__init__()
        self.num_agents = n
        # self.schedule removed in Mesa 3.0, use self.agents
        self.current_price = 100.0
        self.buy_orders = 0
        self.sell_orders = 0
        self.current_news = ""
        
        # News Feed
        self.news_feed = [
            "Tech sector reports record breaking profits!",
            "Uncertainty looms as inflation hits new highs.",
            "Housing market crash predicted by experts.",
            "New trade deal promises economic growth.",
            "Market remains stable with no major changes."
        ]

        # Create Agents
        for _ in range(self.num_agents):
            agent = TraderAgent(self)
            self.agents.add(agent)

        # Data Collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Price": "current_price",
                "News": "current_news",
                "Buys": "buy_orders",
                "Sells": "sell_orders"
            },
            agent_reporters={"Wealth": "wealth"}
        )

    def step(self):
        self.buy_orders = 0
        self.sell_orders = 0
        self.current_news = random.choice(self.news_feed)
        
        # Mesa 3.0 scheduling
        self.agents.shuffle_do("step")
        
        # Price Adjustment
        net_demand = self.buy_orders - self.sell_orders
        self.current_price = self.current_price * (1 + (net_demand * 0.01))
        
        self.datacollector.collect(self)
