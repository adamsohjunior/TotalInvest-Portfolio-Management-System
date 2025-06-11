import random
from datetime import datetime
from cursor import cursor
from simulator.price_simulator import PriceSimulator

ASSETS = {
    'STOCK': [
        {'id': 1,'name': 'Apple Inc', 'code': 'AAPL', 'initial_price': 150.0, 'volatility': 0.18, 'drift': 0.12},
        {'id': 2,'name': 'Microsoft Corporation', 'code': 'MSFT', 'initial_price': 280.0, 'volatility': 0.16, 'drift': 0.11},
        {'id': 3,'name': 'Google LLC', 'code': 'GOOGL', 'initial_price': 130.0, 'volatility': 0.19, 'drift': 0.125},
    ],
    'BOND': [
        {'id': 4,'name': 'US Treasury Bond', 'code': 'USTB', 'initial_price': 100.0, 'volatility': 0.05, 'drift': 0.06},
        {'id': 5,'name': 'Government Bond', 'code': 'GOVBD', 'initial_price': 95.0, 'volatility': 0.04, 'drift': 0.065},
        {'id': 6,'name': 'Corporate Bond AAA', 'code': 'CORPAA', 'initial_price': 98.0, 'volatility': 0.06, 'drift': 0.07},
    ],
    'FUND': [
        {'id': 7,'name': 'S&P 500 Index Fund', 'code': 'SPY', 'initial_price': 400.0, 'volatility': 0.15, 'drift': 0.095},
        {'id': 8,'name': 'Tech Innovators Fund', 'code': 'TECHF', 'initial_price': 250.0, 'volatility': 0.22, 'drift': 0.13},
        {'id': 9,'name': 'Global Equity Fund', 'code': 'GLOBEQ', 'initial_price': 180.0, 'volatility': 0.14, 'drift': 0.09},
    ],
    'COMM': [
        {'id': 10,'name': 'Gold', 'code': 'GOLD', 'initial_price': 1800.0, 'volatility': 0.13, 'drift': 0.06},
        {'id': 11,'name': 'Silver', 'code': 'SLVR', 'initial_price': 23.0, 'volatility': 0.15, 'drift': 0.055},
    ],
    'CASH': [
        {'id': 12,'name': 'Money Market Fund', 'code': 'MMFUND', 'initial_price': 100.0, 'volatility': 0.007, 'drift': 0.025},
        {'id': 13,'name': 'Short-Term Treasury Bills', 'code': 'STBILL', 'initial_price': 100.0, 'volatility': 0.005, 'drift': 0.02},
    ]
}

class Asset:
    def __init__(self, data: dict):
        self.asset_id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.code = data['code']
        self.initial_price = data['initial_price']
        self.drift = data['drift']
        self.volatility = data['volatility'] * 1.05

        # Boost the drift significantly to compensate for bad balancing strategy
        # and choose a few assets to have negative drift to simulate bad performance
        # to get a more diverse range of portfolio performances
        self.drift = data['drift'] + (0.15 if random.random() < 0.35 else -0.45)
        
        self.simulator: PriceSimulator = PriceSimulator(
            self.initial_price,
            self.drift,
            self.volatility
        )

    def next_price(self, current_date: datetime) -> float:
        price: float = self.simulator.step()

        cursor.execute("""
                INSERT INTO AssetPrice (AssetID, MarketPrice, AssetDate)
                VALUES (?, ?, ?);
            """, (self.asset_id, price, current_date))

        return price

    def insert(self) -> None:
        cursor.execute("SET IDENTITY_INSERT Asset ON")
        # Insert the asset into the database
        cursor.execute("""
            INSERT INTO Asset (AssetID, AssetName, Code, AssetType)
            VALUES (?, ?, ?, ?);
        """, (self.asset_id, self.name, self.code, self.type))
        
        if self.type == 'STOCK':
            cursor.execute("""
                INSERT INTO Stock (AssetID, EBITDA, PERatio, EarningPerShare)
                VALUES (?, ?, ?, ?);
            """, (self.asset_id, 100000.00, 25.5, 6.75))

        elif self.type == 'BOND':
            cursor.execute("""
                INSERT INTO Bond (AssetID, InterestRate, MaturityDate)
                VALUES (?, ?, ?);
            """, (self.asset_id, 0.03, '2030-12-31'))
            
        elif self.type == 'FUND':
            cursor.execute("""
                INSERT INTO Fund (AssetID, ExpenseRatio, DividendYield)
                VALUES (?, ?, ?);
            """, (self.asset_id, 0.1, 1.5))

def generate_assets() -> list[Asset]:
    assets = []

    for asset_type, asset_list in ASSETS.items():
        for asset_data in asset_list:
            asset_data['type'] = asset_type
            assets.append(Asset(asset_data))
    
    return assets