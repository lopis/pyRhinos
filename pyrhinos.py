import csv
import datetime

# Dictionary to convert month names into numbers
months = {
    'jan': 1,
    'feb': 2,
    'mrz': 3,
    'apr': 4,
    'mai': 5,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'sept': 9,
    'okt': 10,
    'oct': 10,
    'nov': 11,
    'dec': 12,
    'dez': 12,
}

# Function to convert strings into useful dates
def parseDate(value):
    # First try to convert the date into a number (year)
    # If it fails to convert, then it's not a number
    try:
        value = value.replace('ca ', '').replace('Ca ', '')
        splitVal = value.split(' ')
        if len(splitVal)==2:
            year=int(splitVal[1])
            if year < 10:
                year += 2000
            elif year < 100:
                year += 1900
            month=months[str.lower(splitVal[0])]
        else:
            year = int(value)
            month = 1

        # Assume the 1st of January if only year is present
        return datetime.date(year, month, 1)
    except Exception as e:
        # Convert the date from the format '04.02.1986'
        return datetime.datetime.strptime(value, '%d.%m.%Y').date()

rhinos = {}
with open('data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)

    # Read each row of the CSV and create the rhinos dictionary
    for row in readCSV:
        try:
            newRhino = {}
            newRhino['id'] = row[0]
            newRhino['gender'] = row[1]
            newRhino['birthdate'] = parseDate(row[2])
            newRhino['sire'] = row[3]
            newRhino['dam'] = row[4]
            newRhino['birthplace'] = row[5]
            newRhino['location'] = row[6]
            newRhino['offspring'] = []
            # Add the new rhino to the dictionary
            rhinos[row[0]] = newRhino
        except Exception as e:
            print(e)
            pass

    print('   ')
    print('   ')

    # Do another loop to find offsprings
    for parentId, parent in rhinos.items():
        parent['offspring'] = []
        for childId, child in rhinos.items():
            if child['sire']==parentId or child['dam']==parentId:
                parent['offspring'].append(child)

    # Do another loop to sort the offspring by birth date
    for parentId, parent in rhinos.items():
        parent['offspring'].sort(key = lambda child: child['birthdate'])
        # Then calculate the age gap bewteen them
        ageGapSum = datetime.timedelta()
        prevChildDate = ''
        for child in parent['offspring']:
            if prevChildDate=='':
                prevChildDate = child['birthdate']
            else:
                ageGapSum += (child['birthdate'] - prevChildDate)
        if len(parent['offspring']) > 1:
            parent['avgGap'] = ageGapSum / len(parent['offspring'])
            if parent['avgGap'] > datetime.timedelta(days=50000):
                print(parentId, parent['avgGap'])

    
