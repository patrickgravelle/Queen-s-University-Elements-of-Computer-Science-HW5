# Patrick Gravelle Assignment 5 CISC 101

def readData(filename):
    '''Reads the weather data from the supplied filename. The function returns a list of
dictionaries, where each dictionary consists of the data for a particular month.'''
    # You can see the key names used by examining the code given below.
    fileIn = open(filename, 'r')
    allData = []
    line = fileIn.readline()
    while line != "":
        line = fileIn.readline().strip()
        if line != "":
            values = line.split(',')
            monthData = {}
            monthData['year'] = int(values[0])
            monthData['month'] = int(values[1])
            # yearmonth is a convenience key that is calculated
            monthData['yearmonth'] = int(values[0]) * 100 + int(values[1])
            monthData['meanT'] = float(values[2])
            monthData['maxT'] = float(values[3])
            monthData['minT'] = float(values[4])
            monthData['rain'] = float(values[5])
            monthData['snow'] = float(values[6])
            allData.append(monthData)
    fileIn.close()
    return allData

def showSome(allData):
    '''A convenience function that prints the beginning and end portions of the supplied list.'''
    for i in range(10):
        print(allData[i])
    print("<snip>")
    for i in range(-10, 0):
        print(allData[i])

def getInt(prompt, lowLimit=None, highLimit=None):
    '''A robust function that is sure to return an int value between the two
supplied limits.'''
    numberOK = False
    while not numberOK:
        try:
            userNum = int(input(prompt))
            if lowLimit != None and userNum < lowLimit:
                print("The number must be higher than", lowLimit)
                print("Please try again.")
            elif highLimit != None and userNum > highLimit:
                print("The number must be lower than", highLimit)
                print("Please try again.")
            else:
                numberOK = True
        except ValueError:
            print("Your entry is not a valid integer, please try again.")
    return userNum

def swap(allData, pos1, pos2) :
    allData[pos1], allData[pos2] = allData[pos2], allData[pos1]

def insertionSort(allData, key):
    '''Sorts the supplied list of dictionaries in situ into increasing order
by the key name supplied.'''
    i = 0
    size = len(allData)
    while i < size - 1 :
        smallest = i
        j = i + 1
        while j < size :
            if allData[j][key] < allData[smallest][key] :
                smallest = j
            j = j + 1
        if smallest != i :
            swap(allData, i, smallest)
        i = i + 1
        
def findRain(allData, target):
    '''Uses a binary search to locate rainfall amounts in mm from the supplied list of
dictionaries.  target is a date in the 'yearmonth' value format.  The function assumes
that the list has been sorted by increasing date.  The function will raise a ValueError
exception if the year and month in target do not exist in allData.'''
    low = 0
    high = len(allData) - 1
    while low <= high :
        mid = (low + high) // 2
        if target < allData[mid]['yearmonth'] :
            high = mid - 1
        elif target > allData[mid]['yearmonth'] :
            low = mid + 1
        else :
            return allData[mid]['rain']
    raise ValueError("Target not found.")
    
def findMax(allData, key):
    '''Returns the record from allData that has the maximum value for the supplied key.'''
    insertionSort(allData, key)
    return allData[len(allData)-1]
    
def findMin(allData, key):
    '''Returns the record from allData that has the minimum value for the supplied key.'''
    insertionSort(allData, key)
    return allData[0]

def getAnnualSnow(allData):
    '''This function returns a list of dictionaries which consist of the total
snowfall for every year listed in allData.  Each record will consist of
{'year' : ####, 'totalsnow' : ###.#}, where # is a number.  There will be one record per year.
It does not matter if any month records are missing, the total snowfall is still calculated, by
assuminng zero snow for the missing months.'''
    insertionSort(allData, 'yearmonth')
    totalsnowlist = []
    i = len(allData) - 1
    j = 201200
    while j >= 193800 :
        snowdict = {}
        snowlist = []
        while i >= 0 and allData[i]['yearmonth'] > j :
            snowlist.append(allData[i]['snow'])
            i = i - 1
        totalsnow = sum(snowlist)
        snowdict['year'] = int(j/100)
        snowdict['totalsnow'] = float("{0:.2f}".format(totalsnow))
        j = j - 100
        totalsnowlist.append(snowdict)
    return totalsnowlist

def saveAnnualMeanTemp(allData, filename):
    '''This function calculates the mean temperatures for an entire year and saves this
data to the supplied file - one line in the file per year.
It is assumed that each year from 1938 to 2012 has 12 months.'''
    insertionSort(allData, 'yearmonth')
    meanTempList = []
    i = len(allData) - 1
    j = 201200
    while j >= 193800 :
        meanTdict = {}
        meanTlist = []
        while i >= 0 and allData[i]['yearmonth'] > j :
            meanTlist.append(allData[i]['meanT'])
            i = i - 1
        sumTemp = sum(meanTlist)
        meanTemp = sumTemp/12
        meanTdict['year'] = int(j/100)
        meanTdict['meanTemp'] = float("{0:.2f}".format(meanTemp))
        j = j - 100
        meanTempList.append(meanTdict)
    newfile = open(filename, 'w')
    m = len(meanTempList) - 1
    while m >= 0 :
        line = str(meanTempList[m]) + "\n"
        newfile.write(line)
        m = m - 1
    newfile.close()

def main():
    # Read the data
    db = readData("TorontoWeatherData.csv")
    unsortedDb = readData("TorontoWeatherData.csv")
    # Un-comment these lines to make sure your sort has worked properly.
    print("Before sorting, as read from file:")
    showSome(db)
    insertionSort(db, 'yearmonth')
    print("\nAfter sorting by date:")
    showSome(db)

    # Test your binary search by searching for the rainfall amount for a user-
    # supplied year and month.
    searchYear = getInt("Enter year for rainfall search: ", 1938, 2012)
    searchMonth = getInt("Enter month for rainfall search: ", 1, 12)
    searchYearMonth = 100 * searchYear + searchMonth
    try:
        rainfall = findRain(db, searchYearMonth)
        print(f"Rainfall was {rainfall} mm.")
    except ValueError as message:
        print(message)

    # Test your findMax and findMin functions by locating some extremes.
    # These two functions return a single record which is a dictionary.
    maxR = findMax(db, 'maxT')
    print(f"\nHighest temperature {maxR['maxT']} deg C, in month {maxR['month']}, {maxR['year']}.")
    minR = findMin(db, 'minT')
    print(f"Lowest temperature {minR['minT']} deg C, in month {minR['month']}, {minR['year']}.")
    maxR = findMax(db, 'rain')
    print(f"Highest rainfall {maxR['rain']} mm, in month {maxR['month']}, {maxR['year']}.")
    maxR = findMax(db, 'snow')
    print(f"Highest snowfall {maxR['snow']} cm, in month {maxR['month']}, {maxR['year']}.")

    # annualSnow is a list of dictionaries, where each dictionary holds the year and the total snowfall
    # for that year.
    annualSnow = getAnnualSnow(db)
    insertionSort(annualSnow, 'totalsnow')
    minR = annualSnow[0]
    print(f"\nLowest annual snowfall {minR['totalsnow']} cm, in {minR['year']}.")
    medR = annualSnow[len(annualSnow) // 2]
    print(f"Median annual snowfall {medR['totalsnow']} cm.")    
    maxR = annualSnow[len(annualSnow) - 1]
    print(f"Highest annual snowfall {maxR['totalsnow']} cm, in {maxR['year']}.")
    
    # Sort your data again, by mean temperature this time.  This is the only way you can get the median
    # value, which is defined as the middle of a sorted set of values.
    insertionSort(db, 'meanT')
    minR = db[0]
    print(f"\nLowest mean temperature {minR['meanT']} deg C, in month {minR['month']}, {minR['year']}.")
    medR = db[len(db) // 2]
    print(f"Median mean temperature {medR['meanT']} deg C.")
    maxR = db[-1]
    print(f"Highest mean temperature {maxR['meanT']} deg C, in month {maxR['month']}, {maxR['year']}.")

    # Look for Global Warming!
    saveAnnualMeanTemp(db, "YearMeans.txt")
    
main()
