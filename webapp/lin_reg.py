import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

# global variables
MODEL_DATA_PATH = ('/Users/pallavitangirala/Documents/projects/'
             'budget-recommender/data/budgeted_user_data.csv')
LOCATION_DATA_PATH = ('/Users/pallavitangirala/Documents/projects/'
             'budget-recommender/data/numbeo_col.csv')

# debugging macros
MODEL_EVALUATION = 0
FEATURE_EVALUATION = 0
DEBUG = 0

# indicies in priorities_array input in model
HOUSING_INDEX = 0
TRANSPORTATION_INDEX = 1
FOOD_INDEX = 2
UTILITY_INDEX = 3
INSURANCE_INDEX = 4
HEALTHCARE_INDEX = 5
SAVINGS_INDEX = 6
PERSONAL_SPENDING_INDEX = 7

# budget label
HOUSING_BUDGET = 'Housing Budget'
TRANSPORTATION_BUDGET = 'Transportation Budget'
FOOD_BUDGET = 'Food Budget'
UTILITY_BUDGET = 'Utility Budget'
INSURANCE_BUDGET = 'Insurance Budget'
HEALTHCARE_BUDGET = 'Healthcare Budget'
SAVINGS_BUDGET = 'Savings, Investments, Debt Payments Budget'
PERSONAL_SPENDING_BUDGET = 'Personal Spending Budget'

# index label
COL = 1
RENT = 2
FOOD = 3

# indicies in basic_user_info array

# read dataset
df_model_data = pd.read_csv(MODEL_DATA_PATH)
df_location_data = pd.read_csv(LOCATION_DATA_PATH)

if (FEATURE_EVALUATION):
    # SCATTERPLOT DEV AND DISPLAY
    sns.scatterplot(x='Food Index',
                    y='Food Budget',
                    data=df_model_data)
    plt.show()

def get_basic_user_info(input_income, user_location):
    """
    purpose: to get basic lifestyle info from the user 
    input: NA
    output: an array of basic user information --> 
        (monthly income, cost of living index, rent index, food index)
    details: this will be changed to taking input from front end
    """
    # get user annual income
    # user_annual_income = float(input(
    #     "What is your annual income (Post-tax)? "))
    user_annual_income = float(input_income)
    user_monthly_income = math.trunc(user_annual_income/12)

    # get user location (city, state abbrveation)
    # print("Where are you living? Pick one of the following: ")
    # print(df_location_data['City'].to_string(index=False))
    # user_location = input("Location:" ) # have dropdown for this in ui
    # while (user_location not in df_location_data['City'].values):
    #     user_location = input("Sorry! Please pick a city from the list: ")

    # find location indices based on city
    # user's cost of living index
    user_col_index = df_location_data.loc[df_location_data['City'] == user_location]['Cost of Living Index'].values[0]

    # user's rent index
    user_rent_index = df_location_data.loc[df_location_data['City'] == user_location]['Rent Index'].values[0]

    # user's food index (average of groceries and restaurant)
    user_grocery_index = df_location_data.loc[df_location_data['City'] == user_location]['Groceries Index']
    user_restaurant_index = df_location_data.loc[df_location_data['City'] == user_location]['Restaurant Price Index']
    user_food_index = math.trunc((user_grocery_index.values[0] + user_restaurant_index.values[0])/2)

    if (DEBUG):
        print(user_col_index, user_rent_index, user_food_index)
    
    return user_monthly_income, user_col_index, user_rent_index, user_food_index

def get_user_priorities():
    """
    purpose: get priorities of each budget category from user
    input: NA
    output: an array of priorities of each budget category
    details: this will be changed to taking input from front end
    """
    housing_p = input("What priority is your housing budget? ")
    transportation_p = input("What priority is your transportation budget? ")
    food_p = input("What priority is your food budget (including both groceries and eating out)? ")
    utility_p = input("What priority is your utilities budget? ")
    insurance_p = input("What priority is your insurance budget? ")
    healthcare_p = input("What priority is your healthcare budget? ")
    savings_p = input("What priority is your savings, investments, and debt payments budget? ")
    personal_spending_p = input("What priority is your personal spending budget? ")

    priorities_array = [housing_p, transportation_p, food_p, utility_p, insurance_p, healthcare_p, savings_p, personal_spending_p]
    
    return priorities_array

def find_relevant_info(basic_info, priorities, budget):
    """
    purpose: find relevant info to do with desired budget to calculate
    input:
        - array of user's basic info
        - array of priorities of each budget category (in traditional budget order)
        - desired budget to calculate 
    output: 
        - array of relevant features to find in model dataset --> ('Monthly Income', relevant living index name, priority name)
        - array of relevant user information --> (monthly income, relevant living index value, relevant priority value)
    details: NA
    """
    picker = {
        HOUSING_BUDGET : [HOUSING_INDEX, 'Rent Index', 'Housing Priority', RENT],
        TRANSPORTATION_BUDGET : [TRANSPORTATION_INDEX, 'Cost of Living Index', 'Transportation Priority', COL],
        FOOD_BUDGET : [FOOD_INDEX, 'Food Index', 'Food Priority', FOOD],
        UTILITY_BUDGET : [UTILITY_INDEX, 'Cost of Living Index', 'Utility Priority', COL],
        INSURANCE_BUDGET : [INSURANCE_INDEX, 'Cost of Living Index','Insurance Priority', COL],
        HEALTHCARE_BUDGET : [HEALTHCARE_INDEX, 'Cost of Living Index', 'Healthcare Priority', COL],
        SAVINGS_BUDGET : [SAVINGS_INDEX, 'Cost of Living Index', 'Savings, Investments, Debt Payments Priority', COL],
        PERSONAL_SPENDING_BUDGET: [PERSONAL_SPENDING_INDEX, 'Cost of Living Index', 'Personal Spending Priority', COL]
    } 
    picker_out = picker[budget]
    monthly_income = basic_info[0]
    relevant_index = basic_info[picker_out[3]]
    relevant_priority = priorities[picker_out[0]]

    relevant_features = ['Monthly Income', picker_out[1], picker_out[2]]
    relevant_user_info = [monthly_income, relevant_index]
    relevant_user_info.append(relevant_priority)

    return relevant_features, relevant_user_info

def multilin_reg(desired_budget, features, user_inputs):
    """
    purpose: ml model to predict budget based on user inputs
    input: 
        - desired budget to calculate
        - array of needed features from data to train and test desired budget
        - array of user information to predict budget
    output: budget in dollars for associated category 
    details: multilinear regression model
    """
    # create feature variables
    x = df_model_data[features]
    y = df_model_data[desired_budget]
    feature_names = x.columns.tolist()

    # create train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1, random_state=111)

    # create a regression model
    model = LinearRegression()

    # fitting the model
    model.fit(x_train, y_train)

    # model evaluation
    if (MODEL_EVALUATION):
        # how correlated data is
        print(model.score(x_test, y_test))

        # making predictions based on csv data
        predictions = model.predict(x_test)
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        print('Mean Squared Error', mse)
        print('Mean Absolute Error', mae)

    # make predictions based off input data
    user_inputs = np.array(user_inputs)
    input_df = pd.DataFrame([user_inputs], columns=feature_names)
    prediction = model.predict(input_df)
    return math.trunc(abs(prediction[0]))

def linear_normalization(budgets, monthly_income):
    """
    purpose: make the budgets sum to the monthly income
    input: array of ml model generated budgets, user's monthly income
    output: numpy array of normalized budgets
    details: NA
    """
    coefficients = np.array(budgets)
    desired_sum = monthly_income
    sum_coefficients = np.sum(coefficients)
    normalized_coefficients = (coefficients / sum_coefficients) * desired_sum
    return normalized_coefficients

"""
    ** MAIN ** 
"""
# # get user information and budget priorities
# basic_user_info = get_basic_user_info() # [monthly income, col index, rent index, food index]
# user_priorities = get_user_priorities()

# """
# budget generation
# """
# # HOUSING BUDGET GENERATION
# desired_output = HOUSING_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# housing_output = multilin_reg(desired_output, relevant_features, relevant_user_info)

# # TRANSPORTATION BUDGET GENERATION
# desired_output = TRANSPORTATION_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# transportation_output = multilin_reg(desired_output, relevant_features, relevant_user_info)

# # FOOD BUDGET GENERATION
# desired_output = FOOD_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# food_output = multilin_reg(desired_output, relevant_features, relevant_user_info)

# # UTILITY BUDGET GENERATION
# desired_output = UTILITY_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# utility_output = multilin_reg(desired_output, relevant_features, relevant_user_info)
    
# # INSURANCE BUDGET GENERATION
# desired_output = INSURANCE_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# insurance_output = multilin_reg(desired_output, relevant_features, relevant_user_info)


# # HEALTHCARE BUDGET GENERATION
# desired_output = HEALTHCARE_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# healthcare_output = multilin_reg(desired_output, relevant_features, relevant_user_info)


# # SAVINGS, INVESTMENTS, DEBTS BUDGET GENERATION
# desired_output = SAVINGS_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# savings_output = multilin_reg(desired_output, relevant_features, relevant_user_info)
    

# # PERSONAL SPENDING BUDGET GENERATION
# desired_output = PERSONAL_SPENDING_BUDGET
# relevant_features, relevant_user_info = find_relevant_info(basic_user_info, user_priorities, desired_output)

# if (DEBUG):
#     print(relevant_features[0], relevant_features[1], relevant_features[2])
#     print(relevant_user_info[0], relevant_user_info[1], relevant_user_info[2])

# personal_spending_output = multilin_reg(desired_output, relevant_features, relevant_user_info)

# """
# refining and displaying budgets
# """
# # make budget sum to monthly income
# budget_outputs = [housing_output, transportation_output, 
#                   food_output, utility_output, insurance_output, healthcare_output,
#                   savings_output, personal_spending_output]
# user_monthly_income = relevant_user_info[0]

# # rounding to the nearest int
# adjusted_budgets = linear_normalization(budget_outputs, user_monthly_income)
# housing_final = int(adjusted_budgets[HOUSING_INDEX])
# transportation_final = int(adjusted_budgets[TRANSPORTATION_INDEX])
# food_final = int(adjusted_budgets[FOOD_INDEX])
# utility_final = int(adjusted_budgets[UTILITY_INDEX])
# insurance_final = int(adjusted_budgets[INSURANCE_INDEX])
# healthcare_final = int(adjusted_budgets[HEALTHCARE_INDEX])
# savings_final = int(adjusted_budgets[SAVINGS_INDEX])
# personal_spending_final = int(adjusted_budgets[PERSONAL_SPENDING_INDEX])

# # printing all the budgets
# print(HOUSING_BUDGET,": $", housing_final)
# print(TRANSPORTATION_BUDGET,": $", transportation_final)
# print(FOOD_BUDGET,": $", food_final)
# print(UTILITY_BUDGET, ": $", utility_final)
# print(INSURANCE_BUDGET, ": $", insurance_final)
# print(HEALTHCARE_BUDGET, ": $", healthcare_final)
# print(SAVINGS_BUDGET, ": $", savings_final)
# print(PERSONAL_SPENDING_BUDGET, ": $", personal_spending_final)

