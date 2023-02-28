from faker import Faker
from faker.providers import BaseProvider
from math import trunc
import random
import csv
import pandas

fake = Faker()


class IncomeProvider(BaseProvider):

    def annual_income(self):
        """
        input: None
        output: returns a random income in a range based off of weighted 
        probabilities for each range

        Based off of statistics given by:
        - https://www.statista.com/statistics/203183/percentage-
        distribution-of-household-income-in-the-us/
        - https://dqydj.com/average-median-top-household-income-percentiles/
        """
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
        
        return generated_income

"""
generates weighted random income using annual_income func
"""
fake.add_provider(IncomeProvider)
annual_income = fake.annual_income()
print('Annual Income:', annual_income)

# converting annual to monthly income 
monthly_income = trunc(annual_income/12)
print('Monthly Income:', monthly_income)


"""
generates random location and associated:
    - cost of living index
    - rent index
    - food index
from numbeo_col.csv
"""
df = pandas.read_csv('/Users/pallavitangirala/Documents/projects'
                     '/budget-recommender/data/numbeo_col.csv')

# generating random row number
rand = fake.random_int(0, len(df.index))

print('Location:', df.loc[rand, 'City'])

print('Cost of Living Index:', 
      df.loc[rand, 'Cost of Living Index'])

print('Rent Index:', df.loc[rand, 'Rent Index'])

# food index calculated as average of groceries and restaurant index 
food_index = (df.loc[rand, 'Groceries Index'] 
              + df.loc[rand, 'Restaurant Price Index']) / 2
print('Food Index:', food_index)


"""
budget priority randomly ranked from 1 to 3 
"""
budget_categories = ['Housing & Utility', 'Transportation',
                      'Food', 'Healthcare',
                        'Savings, Investments & Debt Payments',
                          'Personal Spending']
for i in range(0,6):
    print(budget_categories[i],":", fake.random_int(1,3))