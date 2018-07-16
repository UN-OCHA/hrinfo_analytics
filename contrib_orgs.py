'''
Pulls the number of contributing organizations for a given month.
(Does not currently use the API - pulls from admin view)

Setup:
1. Navigate to appropriate web page; must be logged in, must have admin status to see the page.
    (https://www.humanitarianresponse.info/en/admin/contributors/2018/05 - but set proper month in URL)
2. Right click and select "View Page Source" on this page.
3. Copy all and paste into text file. Save text file to same folder as this Python script.
4. Change fields as marked in lines 78 and 79.
'''
import base
from gspread.exceptions import APIError
from collections import Counter

def contrib_orgs(TEXT_FILE, NAME_OF_SHEET):

    lines = [line.rstrip('\n') for line in open(TEXT_FILE)] # read line by line

    try:
        worksheet = base.wks.add_worksheet(title=NAME_OF_SHEET, rows=len(lines), cols=10)
    except APIError:
        worksheet = base.wks.worksheet(NAME_OF_SHEET)

    test = lines[70:]
    index = 0
    orgs = []
    for line in test:
        if "<caption>Name: " in line:
            # ignore admins
            name = line.split('>',2)[2]
            name = name.split('<')[0]
            if name == "Marina Colozzi" or name == "Guillaume Viguier" or name == "Adrian Ciancio":
                index+=1
                continue

            raw_org = test[index+18]
            raw_org =raw_org.strip("</td>")
            raw_org =raw_org.strip("            ")
            if "&#039;" in raw_org:
                raw_org = raw_org.replace("&#039;","'")
            if "," in raw_org:
                raw_orgs = raw_org.split(",")
                for org in raw_orgs:
                    if org[0] == " ":
                        orgs.append(org[1:])
                    else:
                        orgs.append(org)
            else:
                orgs.append(raw_org)
        index+=1

    org_counts = Counter(orgs)
    orgo = org_counts.most_common()
    cells = str(len(orgo))

    # Label
    worksheet.update_acell('A1','Organization')
    worksheet.update_acell('B1','Count')

    # Select a range
    org_list = worksheet.range('A2:A'+cells)
    num_list = worksheet.range('B2:B'+cells)

    index = 0
    for cell in org_list: #update orgs
        cell.value = orgo[index][0]
        index+=1

    index = 0
    for cell in num_list: #update nums
        cell.value = orgo[index][1]
        index+=1

    # Update in batch - to avoid hitting API request limit
    worksheet.update_cells(org_list)
    worksheet.update_cells(num_list)

def main():
    TEXT_FILE = 'june.txt' # CHANGE - to the name of your text file with the source code
    NAME_OF_SHEET = 'June 2018' # CHANGE - to the name of the worksheet in which you want to store the results
    contrib_orgs(TEXT_FILE,NAME_OF_SHEET)

if __name__ == '__main__':
    main()