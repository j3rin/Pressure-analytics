#! /usr/bin/env python3

import json
import sys
import csv
import os.path

#Please use python 3 
def count_contractions(pressure_data):
    """
    Count the number of contractions for a pressure curve

    :param pressure_data: a list of pressure points
    :return: The total number of contractions
    A contraction is valid when the pressure is above 95kPa, then reaches a peak below 85kPa and then reaches a peak again above 95kPa
    """

    firstPeek = False
    secondLow = False
    thirdPeek = False
    count = 0
    for row in pressure_data:
        kPa = float(row[1])
        if(kPa > 95 and firstPeek == False):
            firstPeek = True
        if(kPa < 85 and firstPeek == True and secondLow == False):
            secondLow = True
        if(kPa > 95 and secondLow == True and firstPeek == True):
            thirdPeek = True
        if(firstPeek == True and secondLow == True and thirdPeek == True):
            count = count + 1
            firstPeek = False
            secondLow = False
            thirdPeek = False

    return count

def contractions_per_sec(pressure_data):
    """
    Calculate the mean contractions / secs for a pressure curve

    :param pressure_data: a list of pressure points
    :return: The mean frequency of contraction / secs
    """
    # FIXME
    firstPeek = False
    secondLow = False
    thirdPeek = False
    count = 0
    startTime = 0
    endTime = 0
    times = []
    for row in pressure_data:
        kPa = float(row[1])
        if(kPa > 95 and firstPeek == False):
            firstPeek = True
            startTime = int(row[0])
        if(kPa < 85 and firstPeek == True and secondLow == False):
            secondLow = True
        if(kPa > 95 and secondLow == True and firstPeek == True):
            thirdPeek = True
            endTime = int(row[0])
        if(firstPeek == True and secondLow == True and thirdPeek == True):
            count = count + 1
            firstPeek = False
            secondLow = False
            thirdPeek = False
            times.append(endTime - startTime)

    if(count != 0):
        total = count / (sum(times) / 1000)
    else: 
        total = 0
    return total

def updatePressureJson(pressure_data, contractionCount, contractionPerSec):
    pressureJson = {
        "pressure_points": [],
        "count_contractions": contractionCount,
        "contractions_per_sec": contractionPerSec
    }
    for row in pressure_data:
        ms = float(row[0])
        kPa = float(row[1])
        pressureJson["pressure_points"].append({
            "ms": ms,
            "pressure": kPa
        })
    
    data = json.dumps(pressureJson)
    with open("dashboard/src/pressure.json","w") as f:
        f.write(data)



def main():
    """ 
    I havent optimized the code, the code below could be optimized to remove reptative code
    """
    pressure_file = sys.argv[1]
    #n contraction count & #s is contraction / s
    n = 0
    s = 0
    with open(pressure_file,'rt')as f:
        #skip the first line
        next(f)
        data = csv.reader(f)
        n = count_contractions(data) 
    
    with open(pressure_file,'rt')as f:
        #skip the first line
        next(f)
        data = csv.reader(f)
        s = contractions_per_sec(data) 
    
    with open(pressure_file,'rt')as f:
        next(f)
        data = csv.reader(f)
        updatePressureJson(data, n, s)       
        
    print("---")
    print("For {}:".format(pressure_file))
    print("* Number of contraction = {}".format(n))
    print("* Contraction / s = {}".format(s))

    return 0

if __name__ == '__main__':
    sys.exit(main())
