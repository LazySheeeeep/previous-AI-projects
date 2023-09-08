import scipy.optimize

# Objective function : 50x1 + 80x2
# Constraint 1: 5x1 + 2x2 <= 20
# Constraint 2: -10x1 + -12x2 <= -90

result = scipy.optimize.linprog(
    [50,80],
    A_ub = [[5, 2], [-10, -12]],
    b_ub = [20, -90])

if result.success:
    print(f'X1:{round(result.x[0], 2)}hours')
    print(f'X2:{round(result.x[1], 2)}hours')
