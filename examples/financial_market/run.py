from model import FinancialMarket


def run_simulation():
    # Initialize the model with 10 agents
    model = FinancialMarket(n=10)

    print("Starting Financial Market Simulation...")
    print(f"{'Step':<5} | {'Price ($)':<10} | {'Orders (B/S)':<15} | {'News Headline'}")
    print("-" * 85)

    # Run for 10 steps (simulated days)
    if not model.running:
        print("Simulation stopped: Model not running (likely missing API key).")
        return

    for i in range(10):
        model.step()

        # Get data from the collector
        data = model.datacollector.get_model_vars_dataframe().iloc[-1]

        # Format the output
        price = f"{data['Price']:.2f}"
        orders = f"{data['Buys']} / {data['Sells']}"
        news = data["News"]

        print(f"{i:<5} | {price:<10} | {orders:<15} | {news}")


if __name__ == "__main__":
    run_simulation()
