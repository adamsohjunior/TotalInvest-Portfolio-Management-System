import datetime
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List
from models.asset import Asset
from cursor import cursor


BROKERS = ['AlanBroker', 'CapitalGainz', 'Binanx']

class Portfolio:
    def __init__(self, risk_tolerance: str):
        self.portfolio_id = str(uuid.uuid4())
        self.risk_tolerance = risk_tolerance
        self.status = "ACTIVE"
        self.smart = True if random.random() < 0.45 else False

        self.did_monthly_dca = False
 
        # Set a random start date between 2024-01-01 and 2024-04-10
        self.start_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 5))
        self.asset_allocation = self.get_asset_allocation()

        self.market_value = 0.0
        self.annualised_return = 0.0

        self.topups: List[TopUp] = []

        self.initial_investment = 0.0

        self.owned_assets: List[AssetOwnership] = []

        self.cash_balance = 0.0

    def update_value(self, current_date: datetime, assets: List[Asset]) -> None:
        self.market_value = 0.0
        
        # Calculate market value based on owned assets
        for asset_ownership in self.owned_assets:
            # Find the current price of the asset
            asset_price = 0.0

            for asset in assets:                
                if asset.asset_id == asset_ownership.asset.asset_id:
                    asset_price = asset.simulator.s
                    break

            self.market_value += asset_ownership.quantity * asset_price

        self.market_value += self.cash_balance

        if self.smart:
            self.market_value *= 1.40  # Boost market value for smart portfolios

        total_topups = sum([x.amount for x in self.topups])

        # Calculate annualised return based on current market value
        if total_topups == 0:
            self.annualised_return = 0.0
        else:
            self.annualised_return = ((self.market_value / total_topups) - 1) * 100

        # Update portfolio value in database
        cursor.execute(
            """
            UPDATE Portfolio
            SET MarketValue = ?, AnnualisedReturn = ?
            WHERE PortfolioID = ?
            """, (self.market_value, self.annualised_return, self.portfolio_id)
        )

        # Update total unrealized gain loss in database
        unrealized_gain_loss = (self.market_value - self.cash_balance) - sum([x.purchase_price * x.quantity for x in self.owned_assets])
        cursor.execute("""
            INSERT INTO Unrealised_Gain_Loss (PortfolioID, UGLDate, Amount)
            VALUES (?, ?, ?)
        """, (self.portfolio_id, current_date, unrealized_gain_loss))

        print(f"[{self.portfolio_id}] updated portfolio value: {self.market_value}, annualised return: {self.annualised_return:.2f}%, invested value: {total_topups}, cash balance: {self.cash_balance:.2f}")
        # print(f"[{self.portfolio_id}] unrealized gain/loss: {unrealized_gain_loss:.2f}")

    def balance_portfolio(self, amount: float, assets: List[Asset], current_date: datetime) -> None:        
        # print(f"[{self.portfolio_id}] balancing portfolio with {amount}")

        # Calculate amount to allocate to each asset class
        amount = amount + self.cash_balance

        allocations = {}
        for asset_class, percentage in self.asset_allocation.items():
            allocations[asset_class] = float(percentage) * amount
        
        # For each asset class, buy assets according to allocation
        for asset_class, allocated_amount in allocations.items():
            if allocated_amount < 0.01:  # Skip if amount too small
                continue
                
            # Find assets of this class
            assets_of_class = [asset for asset in assets if asset.type == asset_class]
            if not assets_of_class:
                continue  # Skip if no assets of this class

            # Shuffle assets for randomness
            random.shuffle(assets_of_class)
            
            # Buy assets until allocation is used up
            remaining = allocated_amount
            for asset in assets_of_class[:3]:  # Limit to 3 assets per class for diversification
                asset_price = asset.simulator.s
                if asset_price > remaining:
                    continue
                    
                # Calculate how many units to buy
                units = int(remaining / asset_price)
                if units > 0:
                    self.buy_asset(asset, units, current_date)
                    remaining -= units * asset_price

            self.cash_balance = remaining  # Add any leftover cash to cash balance
        
        # Update asset allocation records in database
        for asset_class, percentage in self.asset_allocation.items():
            allocated_value = float(percentage) * amount
            cursor.execute(
                """
                SELECT PortfolioID FROM Asset_Allocation 
                WHERE PortfolioID = ? AND AssetType = ?
                """, (self.portfolio_id, asset_class)
            )

            if cursor.fetchone():
                # Record exists, update it
                cursor.execute(
                    """
                    UPDATE Asset_Allocation 
                    SET AllocationRatio = ?, AllocatedValue = ?
                    WHERE PortfolioID = ? AND AssetType = ?
                    """, (float(percentage), allocated_value, self.portfolio_id, asset_class)
                )
            else:
                # Record doesn't exist, insert it
                cursor.execute(
                    """
                    INSERT INTO Asset_Allocation (PortfolioID, AssetType, AllocationRatio, AllocatedValue)
                    VALUES (?, ?, ?, ?)
                    """, (self.portfolio_id, asset_class, float(percentage), allocated_value)
                )

    def topup(self, amount: float, current_date: datetime, is_initial: bool = False) -> None:
        print(f"[{self.portfolio_id}] topped up {amount}")

        # self.topups += amount
        if is_initial:
            self.initial_investment += amount

        self.topups.append(TopUp(amount, current_date))

        cursor.execute(
            """
            INSERT INTO PTransaction (TransactionID, PTransactionType, PTransactionDate, Unit, PricePerUnit, PortfolioID)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (uuid.uuid4(), 'TOPUP', current_date.strftime('%Y-%m-%d'), 0, amount, self.portfolio_id))
    
        # Add to invested value
        cursor.execute(
            """
            UPDATE Invested_Value
            SET InvestedValue = InvestedValue + ?, InvestedValueDate = ?
            WHERE PortfolioID = ?
            """, (amount, current_date.strftime('%Y-%m-%d'), self.portfolio_id)
        )


    def buy_asset(self, asset: Asset, quantity: int, purchase_date: datetime) -> None:
        # print(f"[{self.portfolio_id}] bought {quantity} of {asset.asset_id}")

        purchase_price: float = asset.simulator.s
        
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        asset_ownership = AssetOwnership(asset, quantity, purchase_price, purchase_date)
        self.owned_assets.append(asset_ownership)
    
        owned_asset_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO Owned_Assets (OwnedAssetID, Unit, PortfolioID, PurchasePrice)
            VALUES (?, ?, ?, ?)
            """, (owned_asset_id, quantity, self.portfolio_id, purchase_price))
        
        cursor.execute(
            """
            INSERT INTO Bought_Asset_From (OwnedAssetID, AssetID, AssetBroker)
            VALUES (?, ?, ?)
            """, (owned_asset_id, asset.asset_id, random.choice(BROKERS)))

        # Insert transaction into DB
        cursor.execute(
            """
            INSERT INTO PTransaction (TransactionID, PTransactionType, PTransactionDate, Unit, PricePerUnit, PortfolioID)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (uuid.uuid4(), 'BUY', purchase_date.strftime('%Y-%m-%d'), quantity, purchase_price, self.portfolio_id))


    def get_asset_allocation(self) -> None:
        if self.risk_tolerance == 'CONS':
            return {
                'STOCK': Decimal(0.20),
                'BOND': Decimal(0.35),
                'FUND': Decimal(0.15),
                'COMM': Decimal(0.10),
                'CASH': Decimal(0.20)
            }
        elif self.risk_tolerance == 'MODR':
            return {
                'STOCK': Decimal(0.35),
                'BOND': Decimal(0.25),
                'FUND': Decimal(0.20),
                'COMM': Decimal(0.15),
                'CASH': Decimal(0.0)
            }
        else:  # AGGR
           return {
                'STOCK': Decimal(0.45),
                'BOND': Decimal(0.15),
                'FUND': Decimal(0.25),
                'COMM': Decimal(0.12),
                'CASH': Decimal(0.0)
            }


class AssetOwnership:
    def __init__(self, asset: Asset, quantity, purchase_price: float, purchase_date: datetime):
        self.asset: Asset = asset
        self.purchase_price: float = purchase_price
        self.quantity: int = quantity
        self.purchase_date: datetime = purchase_date

class TopUp:
    def __init__(self, amount: float, date: datetime):
        self.amount: float = amount
        self.date: datetime = date