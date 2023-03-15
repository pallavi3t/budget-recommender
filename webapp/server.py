from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from lin_reg import get_basic_user_info, find_relevant_info, multilin_reg, linear_normalization


app = Flask(__name__)
Bootstrap(app)

# budget label
HOUSING_BUDGET = 'Housing Budget'
TRANSPORTATION_BUDGET = 'Transportation Budget'
FOOD_BUDGET = 'Food Budget'
UTILITY_BUDGET = 'Utility Budget'
INSURANCE_BUDGET = 'Insurance Budget'
HEALTHCARE_BUDGET = 'Healthcare Budget'
SAVINGS_BUDGET = 'Savings, Investments, Debt Payments Budget'
PERSONAL_SPENDING_BUDGET = 'Personal Spending Budget'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/input', methods=['POST', 'GET'])
def basicinfo():
    if request.method == 'POST':
        income = request.form['user_income']
        location = request.form['user_location']
        housing_priority = int(request.form['housing'])
        transportation_priority = int(request.form['transportation'])
        food_priority = int(request.form['food'])
        utility_priority = int(request.form['utility'])
        insurance_priority = int(request.form['insurance'])
        healthcare_priority = int(request.form['healthcare'])
        savings_priority = int(request.form['savings'])
        personal_priority = int(request.form['personal'])
        priorities_array = [housing_priority, transportation_priority, food_priority, utility_priority, insurance_priority, healthcare_priority, savings_priority, personal_priority]
        # print(income)
        # print(location)
        # print(housing_priority, transportation_priority, food_priority, utility_priority, insurance_priority, healthcare_priority, savings_priority, personal_priority)

        # applying the ml model
        # finding basic info
        user_monthly_income, user_col_index, user_rent_index, user_food_index = get_basic_user_info(income, location)
        basic_info_array = [user_monthly_income, user_col_index, user_rent_index, user_food_index]

        # housing calc
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        housing_output = multilin_reg(HOUSING_BUDGET, relevant_features, relevant_user_info)

        # transportation calc
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        transportation_output = multilin_reg(TRANSPORTATION_BUDGET, relevant_features, relevant_user_info)

        # food calc
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        food_output = multilin_reg(FOOD_BUDGET, relevant_features, relevant_user_info)

        # utility calc
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        utility_output = multilin_reg(UTILITY_BUDGET, relevant_features, relevant_user_info)

        # insurance calc 
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        insurance_output = multilin_reg(INSURANCE_BUDGET, relevant_features, relevant_user_info)

        # healthcare calc 
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        healthcare_output = multilin_reg(HEALTHCARE_BUDGET, relevant_features, relevant_user_info)

        # savings calc 
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        savings_output = multilin_reg(SAVINGS_BUDGET, relevant_features, relevant_user_info)

        # personal spending calc 
        relevant_features, relevant_user_info = find_relevant_info(basic_info_array, priorities_array, HOUSING_BUDGET)
        personal_output = multilin_reg(PERSONAL_SPENDING_BUDGET, relevant_features, relevant_user_info)

        budget_outputs = [housing_output, transportation_output, food_output, utility_output, insurance_output, healthcare_output, savings_output, personal_output] 
        
        adjusted_budgets = linear_normalization(budget_outputs, user_monthly_income)

        housing_final = int(adjusted_budgets[0])
        transportation_final = int(adjusted_budgets[1])
        food_final = int(adjusted_budgets[2])
        utility_final = int(adjusted_budgets[3])
        insurance_final = int(adjusted_budgets[4])
        healthcare_final = int(adjusted_budgets[5])
        savings_final = int(adjusted_budgets[6])
        personal_final = int(adjusted_budgets[7])
        
        # print('HOUSING FINAL', housing_final)
        # print('TRANSPORTATION FINAL', transportation_final)
        # print('FOOD FINAL', food_final)
        # print('UTILITY FINAL', utility_final)
        # print('INSURANCE FINAL', insurance_final)
        # print('HEALTHCARE FINAL', healthcare_final)
        # print('SAVINGS FINAL', savings_final)
        # print('PERSONAL SPENDING FINAL', personal_final)

        finals = [housing_final, transportation_final, food_final, utility_final, insurance_final, healthcare_final, savings_final, personal_final]

        # finals = {"housing": str(housing_final), "transportation": str(transportation_final), "food": str(food_final), "utility": str(utility_final), "insurance": str(insurance_final), "healthcare":str(healthcare_final), "savings":str(savings_final), "personal": str(personal_final)}

        # return render_template('index.html', housing_final=housing_final, transportation_final=transportation_final, food_final=food_final, utility_final=utility_final, insurance_final=insurance_final, healthcare_final=healthcare_final, savings_final=savings_final, personal_final=personal_final)

        return jsonify(finals)

    else:
        return "GET function has been sent!"


if __name__ == '__main__':
    app.run(debug=True)