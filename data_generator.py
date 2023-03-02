from faker import Faker
from faker.providers import BaseProvider
from math import floor
import random
import pandas as pd 

# global variables
SIZE_DATASET = 5
DF_NUMBEO_LOCATION = pd.read_csv('/Users/pallavitangirala/Documents/projects'
                     '/budget-recommender/data/numbeo_col.csv')
DEBUGGING_MULTIOUT = 0
DEBUGGING_SINGLEOUT = 0

fake = Faker()
# Use Faker to generate other realistic data but isn't useful for model:
# 1) names of users

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
        x = random.uniform(1,100)

        income_breakdown = {
            (1, 9.3) : (0, 15000), 
            (9.3, 17.4) : (15000, 24999),
            (17.4, 25.2) : (25000, 34999),
            (25.2, 36.1) : (35000,49999),
            (36.1, 52.3) : (50000,74999),
            (52.3, 64.2) : (75000,99999), 
            (64.2, 80.1) : (100000, 149999),
            (80.1, 90.4) : (150000,199999),
            (90.4, 95.4) : (200000,349999),
            (95.4, 99.1) : (350000,829999), 
            # ignoring the top 1% of earners
            (99.1, 100) : (830000,3212486)
        }
        for key, value in income_breakdown.items():
            if x > key[0] and x <= key[1]:
                return random.randint(value[0], value[1])

# FUNCTIONS FOR DATA GEN
def income_list_gen(count=SIZE_DATASET):
    """
    purpose: generates lists of random annual and monthly incomes
    input: # of incomes to generate
    output: list of annual incomes and list of monthly incomes
    details: uses custom provider from faker to generate incomes
    """
    annual_out = [fake.annual_income() for n in range(count)]
    monthly_out = [floor(fake.annual_income() / 12) for annual_income in annual_out]

    if (DEBUGGING_MULTIOUT):
        print(', '.join(str(annual_income) for annual_income in annual_out))
        print(', '.join(str(monthly_income) for monthly_income in monthly_out))

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
    location_weights = ([16] + [1] * 2 + [1.5] + [1] * 2 + [8] + [2] + [1] * 9 + [5.5] + [1] * 7 +
                         [3] + [2.5] + [1] * 5 + [5] + [1] * 7 + [2.5] + [1] * 25)
    random_locations = df.sample(count, weights=location_weights, replace=True)
    location_out = random_locations['City'].tolist()
    col_index_out = random_locations['Cost of Living Index'].tolist()
    rent_index_out = random_locations['Rent Index'].tolist()
    food_index_out = random_locations[['Groceries Index', 'Restaurant Price Index']].mean(axis=1).apply(floor).tolist()

    if (DEBUGGING_MULTIOUT):
        print(', '.join(str(location) for location in location_out))
        print(', '.join(str(col_index) for col_index in col_index_out))
        print(', '.join(str(rent_index) for rent_index in rent_index_out))
        print(', '.join(str(food_index) for food_index in food_index_out))

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
    priority_out = [random.randint(1,3) for n in range(count)]
        
    if (DEBUGGING_MULTIOUT):
        print(', '.join(str(priority) for priority in priority_out))

    return priority_out


# CREATE DATAFRAME
# outputs of list generation functions
fake.add_provider(IncomeProvider)
annual_income_list, monthly_income_list = income_list_gen()

(location_list, col_index_list, 
 rent_index_list, food_index_list) = location_index_list_gen()

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
# creating dataframe with newly generated data
df_gendata = pd.DataFrame(data)

if (DEBUGGING_MULTIOUT):
    print(df_gendata)

df_gendata.to_csv('/Users/pallavitangirala/Documents/'
                'projects/budget-recommender/data/user_data.csv')

##############################################################################

#CODE FOR TESTING DATA GEN OUTPUTS

if (DEBUGGING_SINGLEOUT):
    """
    generates weighted random income using annual_income func
    """
    annual_income = fake.annual_income()
    print('Annual Income:', annual_income)

    # converting annual to monthly income 
    monthly_income = floor(annual_income/12)
    print('Monthly Income:', monthly_income)

    """
    generates random location and associated:
        - cost of living index
        - rent index
        - food index
    from numbeo_col.csv
    """
    df = DF_NUMBEO_LOCATION

    # generating random row number
    rand = random.randint(0, len(df.index))

    print('Location:', df.loc[rand, 'City'])

    print('Cost of Living Index:', 
        df.loc[rand, 'Cost of Living Index'])

    print('Rent Index:', df.loc[rand, 'Rent Index'])

    # food index calculated as average of groceries and restaurant index 
    food_index = floor((df.loc[rand, 'Groceries Index'] 
                + df.loc[rand, 'Restaurant Price Index']) / 2)
    print('Food Index:', food_index)


    """
    budget priority randomly ranked from 1 to 3 
    """
    budget_categories = ['Housing', 'Transportation',
                        'Food', 'Utility', 'Healthcare',
                            'Savings, Investments & Debt Payments',
                            'Personal Spending'] # allow for one more goal
    for i in range(0,7):
        print(budget_categories[i],"Priority:", random.randint(1,3))