annual_salary = float(input('Enter the starting salary: '))
total_cost = 1000000
semi_annual_raise = 0.07
low = 0
high = 10000
steps = 0
best_rate = 10000
while low < high-1:
    mid = int((low+high)/2)
    month = 0
    current_savings = 0.0
    salary = annual_salary
    while month < 36:
        if month != 0 and month % 6 == 0:
            salary += salary*semi_annual_raise
        current_savings = (current_savings*0.04)/12 + \
            salary/12*mid/10000+current_savings
        month = month+1
    steps += 1
    if abs(current_savings-total_cost*0.25) < 100:
        best_rate = min(mid, best_rate)
        break
    if current_savings < total_cost*0.25:
        low = mid
    elif current_savings >= total_cost*0.25:
        best_rate = min(mid, best_rate)
        high = mid
        
if(best_rate != 10000):
    print('Best savings rate:%s\nSteps in bisection search: %s\n' %
          (float(best_rate/10000), steps))
else:
    print('It is not possible to pay the down payment in three years.\n')
