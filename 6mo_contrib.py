'''
Pulls the number of unique contributors by organizations from a set of uploaded text files.
Note: Run manually - Does not create a sheet, outputs to console

Text files pulled from HR.info Admin Contributor view per month, and saved in the same folder as this script.
'''
TEXT_FILES = ['jan.txt','feb.txt','march.txt','apr.txt','may.txt','june.txt'] # CHANGE

contributors = set()
for file in TEXT_FILES:
    lines = [line.rstrip('\n') for line in open(file)] # read line by line
    test = lines[70:]
    index = 0
    for line in test:
        if "<caption>Name: " in line:
            name = line.split('>',2)[2]
            name = name.split('<')[0]
            if name == "Marina Colozzi" or name == "Guillaume Viguier" or name == "Adrian Ciancio":
                index+=1
            else:
                contributors.add(name) # add organization name to set if not already in set
        index+=1
print(len(contributors))