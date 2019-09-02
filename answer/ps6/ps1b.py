###########################
# 6.0002 Problem Set 1b: Space Change
# Name:Guo Ziyu
# Collaborators:None
# Time:30 minutes
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

# Problem 1


def dp_make_weight(egg_weights, target_weight, memo={}):
  
    # TODO: Your code here
    dp = []
    dp.append(0)
    for i in range(1, target_weight+1):
        number = []
        for j in egg_weights:
            if i >= j:
                number.append(dp[i-j]+1)
        dp.append(min(number))
    return dp[target_weight]


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    egg_weights = (1, 5, 8)
    n = 15
    print("Egg weights = (1, 5, 8)")
    print("n = 15")
    print("Expected ouput: 3 (5*3)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()