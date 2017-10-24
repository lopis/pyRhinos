import csv

rhinos = {}
with open('data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')

    # Read each row of the CSV and create the rhinos dictionary
    for row in readCSV:
        newRhino = {}
        newRhino['id'] = row[0]
        newRhino['gender'] = row[1]
        newRhino['birthdate'] = row[2]
        newRhino['sire'] = row[3]
        newRhino['dam'] = row[4]
        newRhino['birthplace'] = row[5]
        newRhino['location'] = row[6]
        newRhino['offspring'] = []
        # Add the new rhino to the dictionary
        rhinos[row[0]] = newRhino

    # Do another loop to find offsprings
    for parentId, parent in rhinos.items():
        for childId, child in rhinos.items():
            if child['sire']==parentId or child['dam']==parentId:
                parent['offspring'].append(child)
        print(parent)
