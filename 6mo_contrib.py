'''
Pulls the number of unique contributing organizations from uploaded text files.

Text files pulled from HR.info Admin Contributor view per month.

Instructions:
Right-click and select "View Page Source" on webpage, then copy and paste all into a text file.
Save text file in the same folder as this script.
'''
# UPDATE TEXT_FILES AS NEEDED
TEXT_FILES = ['jan.txt','feb.txt','march.txt','apr.txt','may.txt','june.txt']

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
                # ignore admins
                index+=1
            else:
                # add organization name to set if not already in set
                contributors.add(name)
        index+=1
print(len(contributors))