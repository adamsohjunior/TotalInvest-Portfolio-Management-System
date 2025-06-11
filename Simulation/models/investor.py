import uuid
import random
from pyodbc import Cursor
from models.goal import FinancialGoal
from models.portfolio import Portfolio
from cursor import cursor

INVESTORS_DATA = [
    # Nexlify - include full dataset for better analytics
    ('81234567', 'Ethan Koh', '1990-05-10', 'M', 'ethan.koh@nexlify.com', 'MODR', 85000.00, 'Nexlify'),
    ('84567890', 'Liam Teo', '1995-08-22', 'M', 'liam.teo@nexlify.com', 'AGGR', 65000.00, 'Nexlify'),
    ('85678901', 'Sophie Lim', '1987-11-03', 'F', 'sophie.lim@nexlify.com', 'CONS', 78000.00, 'Nexlify'),
    ('90123456', 'Mason Yap', '1986-04-18', 'M', 'mason.yap@nexlify.com', 'MODR', 89000.00, 'Nexlify'),
    # CapitalWave
    ('82347654', 'Owen Phua', '1990-12-12', 'M', 'owen.phua@capitalwave.com', 'MODR', 81000.00, 'CapitalWave'),
    ('85654321', 'Amelia Ong', '1992-11-01', 'F', 'amelia.ong@capitalwave.com', 'AGGR', 60000.00, 'CapitalWave'),
    ('86743210', 'Julian Koh', '1985-06-15', 'M', 'julian.koh@capitalwave.com', 'CONS', 115000.00, 'CapitalWave'),
    ('89921987', 'Clara Wee', '1998-05-20', 'F', 'clara.wee@capitalwave.com', 'MODR', 72000.00, 'CapitalWave'),
    # BioPulse
    ('87890123', 'Hazel Chew', '1997-01-17', 'F', 'hazel.chew@biopulse.com', 'AGGR', 56000.00, 'BioPulse'),
    ('81239876', 'Lydia Pang', '1990-09-03', 'F', 'lydia.pang@biopulse.com', 'MODR', 93000.00, 'BioPulse'),
    ('87842109', 'Ava Chong', '2003-12-17', 'F', 'ava.chong@biopulse.com', 'AGGR', 58000.00, 'BioPulse'),
    ('88932098', 'Jasper Heng', '1996-05-29', 'M', 'jasper.heng@biopulse.com', 'AGGR', 50000.00, 'BioPulse'),
    # Add investors in their 20s for the gender comparison query
    ('91234567', 'Ryan Lee', '2000-03-15', 'M', 'ryan.lee@nexlify.com', 'AGGR', 62000.00, 'Nexlify'),
    ('92345678', 'Emma Chen', '2001-07-22', 'F', 'emma.chen@nexlify.com', 'AGGR', 60000.00, 'Nexlify'),
    ('93456789', 'Jason Tan', '1999-11-05', 'M', 'jason.tan@capitalwave.com', 'MODR', 58000.00, 'CapitalWave'),
    ('94567890', 'Olivia Wong', '2002-02-28', 'F', 'olivia.wong@capitalwave.com', 'MODR', 55000.00, 'CapitalWave')
]

class Investor:
    def __init__(self, data: tuple):
        self.phone = data[0]
        self.name = data[1]
        self.dob = data[2]
        self.gender = data[3]
        self.email = data[4]
        self.risk_tolerance = data[5]
        self.annual_income = data[6]
        self.company = data[7]
        
        # Deterministic DCA behavior for about 40% of investors
        # Specifically flag some investors as DCA investors based on phone number
        # This ensures we have consistent DCA behavior for specific investors
        phone_last_digit = int(data[0][-1])
        self.does_monthly_dca = phone_last_digit in [1, 2, 3, 4]
        
        # Initialize portfolios (1-3 portfolios per investor)
        self.portfolios: list[Portfolio] = []
        num_portfolios = random.randint(1, 3)
        
        # First portfolio always matches investor's risk tolerance
        self.portfolios.append(Portfolio(self.risk_tolerance))
        
        # Additional portfolios may have different risk tolerances
        for _ in range(num_portfolios - 1):
            random_risk = random.choice(['CONS', 'MODR', 'AGGR'])
            self.portfolios.append(Portfolio(random_risk))

    def insert(self) -> None:
        # Insert investor data into the database
        cursor.execute("""
            INSERT INTO Investor (PhoneNumber, InvestorName, DoB, Gender, Email, RiskTolerance, AnnualIncome, Company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.phone, self.name, self.dob, self.gender, self.email, 
              self.risk_tolerance, self.annual_income, self.company))
        
        # Insert portfolios and their relationship with investor
        for portfolio in self.portfolios:
            goal: FinancialGoal = FinancialGoal(portfolio.start_date)
            
            # Create a goal for each portfolio
            cursor.execute("""
                INSERT INTO Financial_Goal (GoalID, TargetAmount, TargetTimeline, StartDate, GoalType)
                VALUES (?, ?, ?, ?, ?)
            """, (goal.goal_id, goal.target_amount, 
              goal.target_timeline, goal.start_date.strftime('%Y-%m-%d'), goal.goal_type))

            cursor.execute("""
                INSERT INTO Portfolio (PortfolioID, PortfolioStatus, AnnualisedReturn, StartDate, MarketValue)
                VALUES (?, ?, ?, ?, ?)
            """, (portfolio.portfolio_id, portfolio.status, portfolio.annualised_return, 
                 portfolio.start_date, portfolio.market_value))

            # Link investor, goal, and portfolio
            cursor.execute("""
                INSERT INTO Investor_Record (RecordID, GoalID, PortfolioID, PhoneNumber)
                VALUES (?, ?, ?, ?)
            """, (str(uuid.uuid4()), goal.goal_id, portfolio.portfolio_id, self.phone))

            # Add invested value record
            cursor.execute(
                """
                INSERT INTO Invested_Value (PortfolioID, InvestedValueDate, InvestedValue)
                VALUES (?, ?, ?)
                """, (portfolio.portfolio_id, portfolio.start_date.strftime('%Y-%m-%d'), 0.0)
            )
        

def generate_investors() -> list:
    investors = []
    for data in INVESTORS_DATA:
        investor = Investor(data)
        investors.append(investor)
    
    return investors