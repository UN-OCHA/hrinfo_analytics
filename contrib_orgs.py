'''
Pulls the number of contributing organizations for a given month.
(Does not currently use the API - pulls from admin view) - Run manually

Setup:
1. Navigate to appropriate web page; must be logged in, must have admin status to see the page.
    (https://www.humanitarianresponse.info/en/admin/contributors/2018/07 - but set proper month in URL)
2. Right click and select "View Page Source" on this page.
3. Copy all and paste into text file. Save text file to same folder as this Python script.
4. Change fields as marked in lines 89 and 90.
'''
import base
from gspread.exceptions import APIError
from collections import Counter
from datetime import datetime
from pytz import timezone

def contrib_orgs(TEXT_FILE, NAME_OF_SHEET):

    lines = [line.rstrip('\n') for line in open(TEXT_FILE)] # read line by line

    spreadsheet = base.get_spreadsheet()
    try:
        worksheet = spreadsheet.add_worksheet(title=NAME_OF_SHEET, rows=len(lines), cols=10)
    except APIError:
        worksheet = spreadsheet.worksheet(NAME_OF_SHEET)

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
    cells = str(len(orgo)+1)

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # Label
    worksheet.update_acell('A2','Organization')
    worksheet.update_acell('B2','Count')

    # Select a range
    org_list = worksheet.range('A3:A'+cells)
    num_list = worksheet.range('B3:B'+cells)

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
    TEXT_FILE = 'july.txt' # CHANGE - to the name of your text file with the source code
    NAME_OF_SHEET = 'July 2018' # CHANGE - to the name of the worksheet in which you want to store the results
    contrib_orgs(TEXT_FILE, NAME_OF_SHEET)

if __name__ == '__main__':
    main()
