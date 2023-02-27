from faker import Faker
from faker.providers import BaseProvider
from math import trunc
import random

fake = Faker()

class CustomProvider(BaseProvider):

    # # random generation of budget priorty 
    # def budget_priority(self):
    #     return random.choice(["high", "medium", "low"])
    
    # random generation of weighted income by percent distribution
    def monthly_income(self):
        x = fake.pyfloat(positive=True, min_value=1, max_value=100)
        generated_income = 0

        if (x >= 1 and x<= 9.3): 
            generated_income = fake.random_int(0,15000)
        elif (x > 9.3 and x<= 17.4): 
            generated_income = fake.random_int(15000, 24999)
        elif (x > 17.4 and x<= 25.2): 
            generated_income = fake.random_int(25000, 34999)
        elif (x > 25.2 and x<= 36.1): 
            generated_income = fake.random_int(35000,49999)
        elif (x > 36.1 and x<= 52.3): 
            generated_income = fake.random_int(50000,74999)
        elif (x > 52.3 and x<= 64.2): 
            generated_income = fake.random_int(75000,99999)
        elif (x > 64.2 and x<= 80.1): 
            generated_income = fake.random_int(100000, 149999)
        elif (x > 80.1 and x<= 90.4): 
            generated_income = fake.random_int(150000,199999)
        elif (x > 90.4 and x<= 95.4): 
            generated_income = fake.random_int(200000,349999)
        elif (x > 95.4 and x<= 99.1): 
            generated_income = fake.random_int(350000,829999)
        elif (x > 99.1 and x<= 100): 
            #ignoring the top 0.1% of earners
            generated_income = fake.random_int(830,0000,3212486)
        
        return trunc(generated_income/12)

fake.add_provider(CustomProvider)
print("Monthly Income:", fake.monthly_income())

# cost of living index 
print("Cost of Living Index:", fake.random_int(85,184))

budget_categories = ["Housing & Utility", "Transportation", "Food", "Healthcare", "Savings, Investments & Debt Payments", "Personal Spending"]
for i in range(0,6):
    print(budget_categories[i],":", fake.random_int(1,3))