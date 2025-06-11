import random
import math
# import matplotlib.pyplot as plt

class PriceSimulator:
    def __init__(self, s0: float, drift: float, volatiliy: float):
        self.s0 = s0
        self.drift = drift
        self.volatility = volatiliy

        self.T = 0.2 # Time period in years
        self.N = 365
        self.dt = self.T / self.N

        # Current price
        self.s = s0

        # Current time
        self.n = 0

        self.random = random.Random()
        
        self.prices = [0] * self.N

    def get_historic_price(self, n: int):
        if n > self.n:
            raise ValueError("Price can only be calculated for the next time step.")
        
        return self.prices[n]
    
    def step(self) -> float:
        dW = self.random.gauss(0, 1) * (self.dt ** 0.5)
        movement = (self.drift - 0.5 * (self.volatility ** 2)) * self.dt + self.volatility * dW
        self.s *= math.exp(movement)

        # Ensure the price does not drop below 20% of the initial price
        if self.s < self.s0 * 0.2:
            self.s = self.s0 * 0.2

        self.prices[self.n] = self.s
        self.n += 1

        return self.s

# simulator = PriceSimulator(100, 0.05, 0.2)
# for i in range(simulator.N):
#     simulator.step()
# plt.plot(simulator.prices, label='Simulated Price Path')
# plt.title('Simulated Price Path')
# plt.show()