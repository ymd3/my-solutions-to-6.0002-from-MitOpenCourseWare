 ###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_weight = {}
    with open(filename,'r+') as f:
        x = f.readlines()
        for set in x:
            y = set.split(',')
            name = y[0]
            weight = y[1]
            if "\n" in weight:
                weight = list(weight)
                weight.pop(-1)
            cow_weight[name] = int(weight[0])

    return cow_weight


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    keys = []
    for key in cows.keys():
        keys.append(key)
    values = []
    for weight in cows.values():
        values.append(weight)
    values_dis = values.copy()
    values.sort()
    values.reverse()
    make_trip = True
    trips = []
    while make_trip == True:
        name_of_cows = []
        remaining = limit
        copy = values.copy()
        make_trip = False
        for weight in copy:
            if remaining - weight >= 0:
                remaining -= weight
                name_index = values_dis.index(weight)
                name_of_cows.append(keys[name_index])
                keys.pop(name_index)
                values.remove(weight)
                values_dis.remove(weight)
                make_trip = True
        if name_of_cows != []:
            trips.append(name_of_cows)

    return trips



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    keys = []
    for key in cows.keys():
        keys.append(key)
    possibilities = get_partitions(keys)
    least = []

    for key in keys:
        least.append([key])

    for partitions in possibilities:
        feasibility = True

        for trip in partitions:
            total_per_trip = 0

            for cow in trip:
                total_per_trip += cows.get(cow)

            if total_per_trip > limit:
                feasibility = False

        if feasibility == True and len(partitions) < len(least):
            least = partitions

    return least



        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    k = load_cows('ps1_cow_data.txt')
    start = time.time()
    test = greedy_cow_transport(k, 10 )
    x = time.time() - start
    print(f"Time for greedy algorithm: {x}. Number of trips: {len(test)}")
    start = time.time()
    test = brute_force_cow_transport(k, 10)
    x = time.time() - start
    print(f"Time for brute force algorithm: {x}. Number of trips: {len(test)}")

compare_cow_transport_algorithms()
'''The greedy algorithm ran a lot faster had a lot less operations to do. The main thing that 
caused the brute force to be slow was enumerating all the different possibilities that were 
largely not useful, example the extremes with each cow being on a different trip and all cows 
being on one trip. 

The greedy algorithm does not return the optimal solution. It gave 6 instead of 5 from the brute
force. It does so because it finds a locally optimal solution instead of the globally optimal 
solution. 

The brute force does return the optimal solution as it considers all the possible solutions 
to send the cows into space, thus, it will arrive at the best solution. 

ps: I am half assing this part of the problem set because im lazy with explanations. If this 
was an actual uni module that I took, then I certainly would have given it more than a 5 min
effort'''

