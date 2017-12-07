import csv
import datetime
import copy

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

# User friendly names for the columns
isMom = "Dam"
isDad = "Sire"
parentType = "Parent"
rid = "Id"
sex = "Sex"
birthdate = "Birth date"
deathdate = "Date of death"
sire = "Sire"
dam = "Dam"
birthPlace = "Birth place"
location = "Location"
avgGap = "Avg time between calves (years)"
vAge = "Age on first calf (years)"
offspring = "Offspring"
childCount = "Offspring Count"

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
            elif year > 2020 or year < 1945:
                print('Invalid date ' + value)
                raise Exception('Invalid date ' + value)
            month=months[str.lower(splitVal[0])]
        else:
            year = int(value)
            month = 1

        # Assume the 1st of January if only year is present
        return datetime.date(year, month, 1)
    except Exception as e:
        # Convert the date from the format '04.02.1986'
        return datetime.datetime.strptime(value, '%d.%m.%Y').date()

def printToCSV(fileName, parents, fieldnames):
    print(fileName, len(parents))
    out_file = open(fileName, 'w', newline='')
    writer = csv.DictWriter(
        out_file,
        delimiter=';',
        extrasaction='ignore',
        fieldnames=fieldnames
    )
    writer.writeheader() # Write the header first
    for parent in parents:
        writer.writerow(parent) # Write each parent
        for child in parent[offspring]:
            writer.writerow(child) # Followed by each child of hers
    out_file.close()

rhinos = {}
parents = []
moms = []
dads = []
stats = {
    'institutions': {},
    'sexes': {},
    'baby_sex': {},
    'wild_moms': []
}
with open('data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)

    # Read each row of the CSV and create the rhinos dictionary
    for row in readCSV:
        try:
            newRhino = {}
            newRhino[rid] = row[0]
            newRhino[sex] = row[1]
            newRhino[birthdate] = parseDate(row[2])
            newRhino[sire] = row[3]
            newRhino[dam] = row[4]
            newRhino[birthPlace] = row[5]
            newRhino[location] = row[6] if len(row[6]) > 0 else row[5]
            newRhino[avgGap] = 0
            newRhino[vAge] = ''
            newRhino[offspring] = []
            # Add the new rhino to the dictionary
            rhinos[row[0]] = newRhino
            # Update location stats:
            if not newRhino[location] in stats['institutions']:
                stats['institutions'][newRhino[location]] = 0
            stats['institutions'][newRhino[location]] += 1
            # Gender stats
            if not newRhino[sex] in stats['sexes']:
                stats['sexes'][newRhino[sex]] = 0
            stats['sexes'][newRhino[sex]] += 1
        except Exception as e:
            print('Exception', e)
            pass

    print('   ')
    print('   ')

    # Do another loop to find offsprings
    for parentId, parent in rhinos.items():
        parent[offspring] = []
        for childId, child in rhinos.items():
            if child[dam]==parentId or child[sire]==parentId:
                parent[offspring].append(copy.copy(child))

    # Do another loop to sort the offspring by birth date
    for parentId, parent in rhinos.items():
        parent[offspring].sort(key = lambda child: child[birthdate])
        # Then calculate the age gap bewteen them
        ageGapSum = datetime.timedelta()
        prevChildDate = ''
        for child in parent[offspring]:
            if prevChildDate=='':
                parent[vAge] = "{:.1f}".format((child[birthdate] - parent[birthdate]).days / 365).replace('.', ',')
            else:
                ageGapSum += (child[birthdate] - prevChildDate)
            prevChildDate = child[birthdate]
            # Update babz gender stats
            if not child[sex] in stats['baby_sex']:
                stats['baby_sex'][child[sex]] = 0
            stats['baby_sex'][child[sex]] += 1
        if len(parent[offspring]) > 1:
            # parent[avgGap] = "{:.1f}".format((ageGapSum / len(parent[offspring])).days / 365).replace('.', ',')
            parent[avgGap] = "{:.1f}".format((ageGapSum / (len(parent[offspring]) - 1)).days / 365).replace('.', ',')
        if len(parent[offspring]) > 0:
            parent[childCount] = len(parent[offspring])
            parent[parentType] = isDad if parent[sex] == 'm' else isMom
            # parents.append(parent)
            if parent[sex] == 'f':
                moms.append(parent)
                if parent[dam] == 'wild':
                    stats['wild_moms'].append(parent[rid])
            elif parent[sex] == 'm':
                dads.append(parent)

    fieldnames = [
        parentType,
        rid,
        sex,
        birthdate,
        sire,
        dam,
        birthPlace,
        location,
        avgGap,
        vAge,
        childCount
    ]

    printToCSV('dads.csv', dads, fieldnames)
    printToCSV('moms.csv', moms, fieldnames)

    # Print stats:
    print('institutions:', stats['institutions'], '\n')
    print('sexes:', stats['sexes'], '\n')
    print('baby sexes:', stats['baby_sex'], '\n')
    print('mom count:', len(moms), '\n')
    print('wild moms:', stats['wild_moms'], 'Total:', len(stats['wild_moms']), '\n')
