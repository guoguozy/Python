annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(
    input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
current_savings = 0.0
month = 0
while current_savings < (total_cost*0.25):
    current_savings = (current_savings*0.04)/12 + \
        annual_salary/12*portion_saved+current_savings
    month = month+1
print('Number of months:%s\n'% month)
