from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/basicinfo', methods=['POST', 'GET'])
def basicinfo():
    if request.method == 'POST':
        income = request.form['user_income']
        location = request.form['user_location']
        print(income)
        print(location)
        return "Received POST request!"
    else:
        return "This is a GET request"
    
@app.route('/priorities', methods=['POST', 'GET'])
def budget_priorities():
    if request.method == 'POST':
        housing_priority = int(request.form['housing'])
        transportation_priority = int(request.form['transportation'])
        food_priority = int(request.form['food'])
        utility_priority = int(request.form['utility'])
        insurance_priority = int(request.form['insurance'])
        healthcare_priority = int(request.form['healthcare'])
        savings_priority = int(request.form['savings'])
        personal_priority = int(request.form['personal'])
        print(housing_priority, transportation_priority, food_priority, utility_priority, insurance_priority, healthcare_priority, savings_priority, personal_priority)
        return "Received POST request!"
    else:
        return "This is a GET request"

if __name__ == '__main__':
    app.run(debug=True)