import mesa
from mesa_llm.module_llm import ModuleLLM

class TraderAgent(mesa.Agent):
    """
    Trader Agent that uses the built-in ModuleLLM for decision making.
    """
    def __init__(self, model):
        super().__init__(model)
        self.cash = 1000
        self.stocks = 10
        
        # USE THE BUILT-IN MODULE INSTEAD OF CUSTOM CLIENT
        self.llm = ModuleLLM(
            llm_model="openai/gpt-3.5-turbo",
            system_prompt="You are a financial trading bot. Reply with exactly one word: BUY, SELL, or HOLD."
        )

    @property
    def wealth(self):
        return self.cash + (self.stocks * self.model.current_price)

    def step(self):
        news = self.model.current_news
        
        # Construct the prompt
        prompt = (
            f"Analyze this news headline: '{news}'. "
            f"Decide if you should BUY, SELL, or HOLD. "
        )
        
        # Use the built-in generation method
        try:
            decision = self.llm.generate(prompt)
             # litellm returns a ModelResponse object, but ModuleLLM.generate returns the string content directly?
             # Let's double check ModuleLLM.generate implementation.
             # Wait, looking at ModuleLLM code again from step 14:
             # return response
             # and response = completion(...)
             # completion returns a ModelResponse object.
             # So I probably need to access choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            decision = "HOLD"
            
        # We need to handle the response object correctly.
        # However, checking the ModuleLLM.generate in step 14: 
        # It returns 'response'.
        # Let's assume standard litellm response format for now and adjust if needed during validaton.
        # Actually, let's verify if I should strip it here or if ModuleLLM does it.
        # ModuleLLM does NOT strip it.
        
        if hasattr(decision, 'choices'):
             decision = decision.choices[0].message.content
        
        decision = str(decision).strip().upper()

        # Execute Trade
        price = self.model.current_price
        if "BUY" in decision and self.cash >= price:
            self.cash -= price
            self.stocks += 1
            self.model.buy_orders += 1
        elif "SELL" in decision and self.stocks > 0:
            self.cash += price
            self.stocks -= 1
            self.model.sell_orders += 1
