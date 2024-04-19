###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight == 0:
        memo[0] = 0
        return 0

    else:
        try:
            return memo[target_weight]

        except KeyError:
            for values in range(len(egg_weights)):      #why does it not go on to the value of egg weights = 5
                if target_weight - egg_weights[values] == 0:
                    memo[target_weight] = 1
                    return 1

                if target_weight - egg_weights[values] > 0:
                    previous = dp_make_weight(egg_weights, target_weight - egg_weights[values], memo)
                    memo[target_weight] = previous + 1

            return memo.get(target_weight)








def brute_force(egg_weights, target_weight, memo = {}):
    '''using brute force and no dynamic programming. '''
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

''' why it would be difficult to use a brute force algorithm with 30 different egg weights?
It is hard as for every egg weight, it would have to find a solution to it depending on the size
of the target weight. This means that the computer would have to solve every target weight value 
that is lower than the target weight all the way to the zero value, giving it an exponential worse
case scenario growth. Hence, as the number of eggs grow, the number of operations grow so exponentially 
that without dynamic programming, the programme efficiency would be very low'''

'''implement a greedy algorithm.
objective function would be to find the least number of eggs. The constraints would be the target weight.
The greedy algorithm would take the largest value and minus it from the target weight and continue to do
so until it is unable to, and then checks the remaining eggs values and then continue the same process. 
'''

'''no it would not always give the optimal solution. eggs = 15,6,1. target weight = 20
solution would pick 15 first then 5 of 1 giving 6. brute force givies 3 of 6 and 2 of 1, giving a total 
of 1.'''