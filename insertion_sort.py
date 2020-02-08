# insertion_sort.py: runs the insertion_sort alogrithm on a series of randomly
#                    generated lists. Then inputs the data into a csv file.
#
# Author: Justin D. Selsor
# Date: 02-07-2020
#
# To run this script use the following commands
#   $ python3 insertion_sort.py
# The script will ask for input:
#   For a size (n) for the lists.
#   A range of values (lower_bounds, upper_bounds).
#   Amount of lists to generate.
# The script will output:
#   a .csv file named "T_n_range_date_time.csv" where:
#       T: the total amount of lists generated.
#       n: the size of each list.
#       range: the range of possabile values for the elements of each list.
#       date: the date the file was generated.
#       time: the time the file was generated.

import random
import time
import sys
import os
import csv

from math import floor, ceil
from threading import Thread
from datetime import datetime

amt_left = -1
amt_done = 0

# Returns a random list of size n with elements being in the
# range of lower_bounds and upper_bounds.
#
# lower_bounds: is the lower bounds of range of elements.
# upper_bounds: is the upper bounds of range of elements.
# n: is the size of the list to be generated.
def create_random_list (lower_bounds, upper_bounds, n):
    l = []
    for i in range(n):
        l.append (random.randint(int(lower_bounds), int(upper_bounds)))
    random.shuffle(l)
    return l

# swaps two elements of a list (l).
# l: any list
# a: index of element 1
# b: index of element 2
def swap (l, a, b):
    if a == b:
        return
    temp = l[a]
    l[a] = l[b]
    l[b] = temp

# returns the complexity(c) of the list l.
# l: is any list
# s: is l but sorted
# returns: c where 0<=c<=1
def get_complexity (l, s):
    l_dot_s = sum(map (lambda x, y: x * y, l, s))
    s_dot_s = sum(map (lambda y: y * y, s))
    return l_dot_s / s_dot_s

# using the insertion_sort algorthim sorts the list l.
# and returns the number of iterations it took.
def insertion_sort (l):
    i = 1
    iterations = 1
    while i < len(l):
        j = i
        while j > 0 and l[j-1] > l[j]:
            iterations += 1
            swap (l, j, j-1)
            j -= 1
        i += 1
    return iterations

# Creates the data and inputs it into a csv file.
# colums: is the length of the csv file - 1 (header row)
# lower_bounds: the lower bounds for elements in a list
# upper_bounds: the upper bounds for elements in a list
# length: the length of any list (if r then each list is a random length [3,inf]
# outputs: a csv file.
def create_csv_file (colums, lower_bounds, upper_bounds, length):
    global amt_left, amt_done

    file_name = colums + '_' + length + '_' + lower_bounds + 'x' + upper_bounds + '_' + length + '_' + datetime.now().strftime('%d-%m-%Y_%H:%M:%S') + '.csv'

    with open (file_name, 'w', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow ([
            'Input List', 
            'Sorted Input List', 
            'Total Iteration',
            'Complexity of Input List',
            'Time Taken (s)'
        ])

    l = []
    while (amt_done <= amt_left):
        rnd_n = random.randint(0, 3000)
        l = create_random_list (
                lower_bounds,
                upper_bounds,
                rnd_n if length=='r' else int(length)
            )

        # Collect the Data
        copy_l = list(l)
        sTime = time.time()
        iterations = insertion_sort(copy_l)
        eTime = time.time()
        complexity = get_complexity (l, copy_l)
        total_time = eTime - sTime

        # Package the Data
        with open(file_name, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([
                copy_l,
                l,
                iterations,
                complexity,
                total_time
            ])

        printProgressBar (amt_done, int(colums), prefix = 'Progress:', suffix = 'Complete', length=50)
        amt_done += 1

    os.system('mv *.csv ../data')

# Prints a Progress Bar to the Console.
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd='\r'):
    percent = (
                "{0:." + str(decimals) + "f}"
            ).format(100 * (iteration / float(total)))

    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print ('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    if iteration == total:
        print()
        print()

if __name__ == '__main__':
    # Get values for iterations
    os.system('clear')

    cols = input ("Input length csv data: ")
    lowbounds = input ("Input lower bounds for list elements: ")
    upbounds = input ("Input upper bounds for list elements: ")
    n = input (
        "Input length of each list (use r for list to have a random length): "
        )

    amt_left = int (cols)
    
    os.system ('clear')
    printProgressBar (0, amt_left, prefix = 'Progress:', suffix = 'Complete', length=50)

    Thread(target = create_csv_file, kwargs=dict(
        colums=cols,
        lower_bounds = lowbounds,
        upper_bounds = upbounds,
        length = n,
    )).start()
