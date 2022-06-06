import csv
import pandas as pd
from csv import reader
from csv import writer
import numpy as np
from numpy import genfromtxt


def test():
    array = np.loadtxt('result.csv', delimiter=',', dtype='str')
    array = np.char.split(array)

    for datas in array:
        for index, data in enumerate(datas):
            count = 0
            five = 0
            four = 0
            zero = 0
            check = True
            for i in range(0, len(datas) - 1, ):
                if check == False:
                    break;
                else:
                    for h in range(i + 1, i + 2):
                        if datas[i] == datas[h]:
                            if datas[i] == "5":
                                five += 1
                            elif datas[i] == '4':
                                four += 1
                            elif datas[i] == '0':
                                zero += 1
                            if check_condition(five, four, zero) == False:
                                check = False
                                break;
            print('five: ' + str(five))
            print('four: ' + str(four))
            print('zero: ' + str(zero))
            if five >= 3 and four >= 3 and zero >=3:
                print('hit\n')
            break

def check_condition(five, four, zero):
    if five >=2:
        return True
    if four >=3:
        return False
    if zero >=3:
        return False
