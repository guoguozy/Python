###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:GuoZiyu
# Collaborators:None
# Time: 30 minutes

from ps1_partition import get_partitions
import time

# ================================
# Part A: Transporting Space Cows
# ================================

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
    # TODO: Your code here
    result_dict = {}
    with open(filename) as file_object:
        lines = file_object.readlines() # 按行读取文件

    for line in lines:
        list = line.split(',', 2)# 将每行以逗号为间隔分开
        result_dict[list[0]] = int(list[1])#写入字典
    return result_dict
# Problem 2


def greedy_cow_transport(cows, limit=10):
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
    # TODO: Your code here
    result_list = []
    cows_copy = cows.copy()#用于记录真正的放置情况
    while len(cows_copy) > 0:#物品真正放置完毕
        list = []
        cows_another_copy = cows_copy.copy()#用于取出最大的且能放置的物品
        heavy = 0
        while len(cows_another_copy) > 0:#
            if cows_another_copy[max(cows_another_copy, key=cows_another_copy.get)] <= limit-heavy:
                list.append(max(cows_another_copy, key=cows_another_copy.get))#符合条件即放置
                heavy = heavy + \
                    cows_copy[max(cows_another_copy,
                                  key=cows_another_copy.get)]
                del cows_copy[max(cows_another_copy,
                                  key=cows_another_copy.get)]# 在真正放置的dict中去掉已放置的
            del cows_another_copy[max(
                cows_another_copy, key=cows_another_copy.get)]# 不管是否放置都去掉
        result_list.append(list)
    return result_list

# Problem 3


def brute_force_cow_transport(cows, limit=10):
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
    # TODO: Your code here
    best_transport = []
    min_trip = len(cows)
    for partition in get_partitions(cows.keys()):
        flag = True
        for i in partition:
            heavy = 0
            for j in i:
                heavy = heavy+cows[j]
            if heavy > limit:
                flag = False
        if flag == True and len(partition) < min_trip:
            best_transport = partition
            min_trip = len(partition)
    return best_transport
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
    # TODO: Your code here
    cows_dict = load_cows('ps1_cow_data.txt')
    start = time.time()
    greedy_cow_transport(cows_dict)
    end = time.time()
    print('Greed_cow_transport:\nTrip number:', len(greedy_cow_transport(
        cows_dict)), 'Running Time:', end-start)

    start = time.time()
    brute_force_cow_transport(cows_dict)
    end = time.time()
    print('Brute_force_cow_transport:\nTrip number:', len(brute_force_cow_transport(
        cows_dict)), 'Running Time:', end-start)


if __name__ == '__main__':
    compare_cow_transport_algorithms()