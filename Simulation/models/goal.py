import random
import uuid
import datetime

GOAL_TYPES = ["First Home Purchase", "Children's Education", "Early Retirement", "Financial Independence", 
              "Travel Fund", "Emergency Fund", "Business Startup", "Medical Expenses"]

GOAL_WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.08, 0.05, 0.04, 0.03]

class FinancialGoal:
    def __init__(self, date: datetime.datetime):
        self.goal_id = str(uuid.uuid4())
        self.goal_type = random.choices(GOAL_TYPES, weights=GOAL_WEIGHTS, k=1)[0]
        self.target_amount = round(random.uniform(100000, 1000000), 2)
        self.target_timeline = (datetime.datetime(2024, 1, 1)+ datetime.timedelta(days=random.randint(365*5, 365*20))).strftime('%Y-%m-%d')
        self.start_date = date

    def to_sql_insert(self):
        return \
            f"""
            INSERT INTO Financial_Goal (GoalID, TargetAmount, TargetTimeline, StartDate, GoalType)
            VALUES ('{self.goal_id}', {self.target_amount}, '{self.goal_type}', '{self.target_timeline}', '{self.start_date}');
            """