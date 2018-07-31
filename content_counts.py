'''
Pulls counts of content types for all organizations - automated
In conjunction with doc_counts, map_counts, event_counts, and assess_counts
'''
import base
from gspread.exceptions import APIError
from datetime import datetime
from pytz import timezone
import list_orgs

def collect_orgs(content, org_info):
    for org in content['data']:
        org_info.append((org['id'],org['label']))
    return content, org_info

def next_page(content, count):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        count += len(content['data'])
        content, count = next_page(content, count)
    except KeyError:
        pass
    return content, count

def update_timestamp(worksheet):
    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "As of: " + formatted_time + ' (GMT+2)'
    return updated

def content():
    org_info = list_orgs.main()
    num_orgs = len(org_info)
    rows = str(num_orgs+2)

    # open sheet
    try:
        worksheet = base.wks.add_worksheet(title="Content By Org", rows=(num_orgs+4), cols=10)
        # label
        worksheet.update_acell('A2','Organization')
        worksheet.update_acell('B2','Documents')
        worksheet.update_acell('C2','Maps/Infographics')
        worksheet.update_acell('D2','Events')
        worksheet.update_acell('E2','Assessments')
        worksheet.update_acell('F2','Total Content')
    except APIError:
        worksheet = base.wks.worksheet("Content By Org")

    # organizations
    name_cells = worksheet.range('A3:A'+rows)
    index = 0
    for cell in name_cells:
        cell.value = org_info[index][1]
        index+=1
    worksheet.update_cells(name_cells)

    return num_orgs, org_info, worksheet, rows

def main():
    content()

if __name__ == '__main__':
    main()