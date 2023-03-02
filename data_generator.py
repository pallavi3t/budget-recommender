from faker import Faker
from faker.providers import BaseProvider
from math import floor
import pandas as pd 

# global variables
SIZE_DATASET = 5
DF_NUMBEO_LOCATION = pd.read_csv('/Users/pallavitangirala/Documents/projects'
                     '/budget-recommender/data/numbeo_col.csv')

fake = Faker()

# class for customizing income generation
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
 
fake.add_provider(IncomeProvider)


# FUNCTIONS FOR DATA GEN

def income_list_gen(count=SIZE_DATASET):
    """
    purpose: generates lists of random annual and monthly incomes
    input: # of incomes to generate
    output: list of annual incomes and list of monthly incomes
    details: uses custom provider from faker to generate incomes
    """
    annual_out = []
    monthly_out = []
    for n in range (count):

        # take annual from user 
        annual_income= fake.annual_income()

        # use monthly to aid in personal calculation of budget
        monthly_income = floor(fake.annual_income() / 12)

        annual_out.append(annual_income)
        monthly_out.append(monthly_income)

        #print(annual_income, monthly_income)

    return annual_out, monthly_out

def location_index_list_gen(df=DF_NUMBEO_LOCATION, count=SIZE_DATASET):
    """
    purpose: generate list of random locations with lists of associated: 
        cost of living index
        rent index 
        food index
    input: # of locations and associated indices to generate
    output: 4 lists of locations with associated 3 indicies
    details: food index is average of grocery and restaurant index
    """
    location_out = []
    col_index_out = []
    rent_index_out = []
    food_index_out = []

    for n in range(count):
        rand = fake.random_int(0, len(df.index))

        location = df.loc[rand, 'City']
        col_index = df.loc[rand, 'Cost of Living Index']
        rent_index = df.loc[rand, 'Rent Index']
        food_index = floor((df.loc[rand, 'Groceries Index'] 
              + df.loc[rand, 'Restaurant Price Index']) / 2)
        
        location_out.append(location)
        col_index_out.append(col_index)
        rent_index_out.append(rent_index)
        food_index_out.append(food_index)

        #print(location, col_index, rent_index, food_index)

    return location_out, col_index_out, rent_index_out, food_index_out


def priority_list_gen(count=SIZE_DATASET):
    """
    purpose: generates list of random priorities
    input: # of priorites to generate
    output: list of random priorities
    details: priorities are identified by integer 1-3
        high priority --> 1
        medium priority --> 2
        low priority --> 3
    """
    out = []
    for n in range (count):
        priority= fake.random_int(1,3)
        out.append(priority)
        #print(priority)

    return out


# CREATE DATAFRAME

# outputs of list generation functions
annual_income_list, monthly_income_list = income_list_gen()

location_list, col_index_list, rent_index_list, food_index_list = location_index_list_gen()

housing_p_list = priority_list_gen()
transportation_p_list = priority_list_gen()
food_p_list = priority_list_gen()
utility_p_list = priority_list_gen()
healthcare_p_list = priority_list_gen()
savings_p_list = priority_list_gen()
personal_p_list = priority_list_gen()

data = {'Annual Income': annual_income_list,
        'Monthly Income':monthly_income_list,
        'Location':location_list,
        'Cost of Living Index':col_index_list,
        'Rent Index':rent_index_list,
        'Food Index':food_index_list,
        'Housing Priority':housing_p_list,
        'Transportation Priority':transportation_p_list,
        'Food Priority':food_p_list,
        'Utility Priority':utility_p_list,
        'Healthcare Priority':healthcare_p_list,
        'Savings, Investments, Debt Payments Priority':savings_p_list,
        'Personal Spending Priority':personal_p_list}


# EXPORTING TO CSV
#df = pd.DataFrame(data)

# CODE FOR TESTING DATA GEN OUTPUTS

# """
# generates weighted random income using annual_income func
# """
# annual_income = fake.annual_income()
# print('Annual Income:', annual_income)

# # converting annual to monthly income 
# monthly_income = floor(annual_income/12)
# print('Monthly Income:', monthly_income)

# """
# generates random location and associated:
#     - cost of living index
#     - rent index
#     - food index
# from numbeo_col.csv
# """
# df = pd.read_csv('/Users/pallavitangirala/Documents/projects'
#                      '/budget-recommender/data/numbeo_col.csv')

# # generating random row number
# rand = fake.random_int(0, len(df.index))

# print('Location:', df.loc[rand, 'City'])

# print('Cost of Living Index:', 
#       df.loc[rand, 'Cost of Living Index'])

# print('Rent Index:', df.loc[rand, 'Rent Index'])

# # food index calculated as average of groceries and restaurant index 
# food_index = floor((df.loc[rand, 'Groceries Index'] 
#               + df.loc[rand, 'Restaurant Price Index']) / 2)
# print('Food Index:', food_index)


# """
# budget priority randomly ranked from 1 to 3 
# """
# budget_categories = ['Housing', 'Transportation',
#                       'Food', 'Utility', 'Healthcare',
#                         'Savings, Investments & Debt Payments',
#                           'Personal Spending'] # allow for one more goal
# for i in range(0,7):
#     print(budget_categories[i],"Priority:", fake.random_int(1,3))