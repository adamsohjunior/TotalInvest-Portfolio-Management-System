import datetime
import random
from typing import List
from models.asset import Asset, generate_assets
from models.investor import Investor, generate_investors
from cursor import conn

START_DATE = datetime.datetime(2024, 1, 1)
DAYS = 365

def simulate():
    investors: List[Investor] = generate_investors()
    assets: List[Asset]  = generate_assets()

    for investor in investors:
        investor.insert()

    for asset in assets:
        asset.insert()

    # focus = investors[0].portfolios[0]

    for day in range(DAYS):
        today = START_DATE + datetime.timedelta(days=day)
        print("Simulating day:", today.strftime("%Y-%m-%d"))

        # Simulate today's asset prices
        for asset in assets:
            asset.next_price(today)

        if day == 100:
            pass
        
        # Simulate investor transactions
        for investor in investors:
            for portfolio in investor.portfolios:
                # Skip portfolios that are not yet active
                if portfolio.start_date > today:
                    continue

                elif portfolio.start_date == today:
                    # Do initial deposit, 20% of annual income
                    initial_deposit = investor.annual_income * 0.2
                    portfolio.topup(initial_deposit, today, is_initial=True)

                     # Balance portfolio after topup
                    portfolio.balance_portfolio(initial_deposit, assets, today)

                    continue

                if today.day == 1:
                    # Reset monthly DCA flag
                    portfolio.did_monthly_dca = False

                # Simulate random transaction, for now just topup
                should_deposit = \
                random.random() < (0.05 + 
                    (0.90 if (investor.does_monthly_dca and today.day <= 7 and not portfolio.did_monthly_dca) else 0))
            
                if not portfolio.did_monthly_dca and should_deposit:
                    portfolio.did_monthly_dca = True

                if should_deposit:
                    amount_to_deposit = (investor.annual_income / 12) * random.uniform(0.05, 0.10)
                    portfolio.topup(amount_to_deposit, today)

                    # Balance portfolio after topup
                    portfolio.balance_portfolio(amount_to_deposit, assets, today)

                # Update portfolio value and unrealized gain loss for the day
                portfolio.update_value(today, assets)
                
            
            conn.commit()

if __name__ == "__main__":

    # Simulate the investment process
    simulate()
    conn.commit()