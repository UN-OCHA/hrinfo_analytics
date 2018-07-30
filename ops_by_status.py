'''
Lists operations by status, as well as the date each operation was last modified. - automated
'''

import base
from gspread.exceptions import APIError
import time
from datetime import datetime
from pytz import timezone

def next_page(content,op_status):
    try:
        url = content['next']['href']
        content = base.open_url(url)
        op_status = op_stat(content, op_status)
        op_status = next_page(content, op_status)
    except KeyError:
        pass
    return op_status

def op_stat(content, op_status):
    for operation in content['data']:
        last_modified = time.strftime("%Y %d %b", time.localtime(int(operation['changed'])))
        op_status[operation['label']] = (operation['status'], last_modified)
    return op_status

def ops_by_status(url):
    content = base.open_url(url)
    op_status = {}
    op_status = op_stat(content, op_status)
    op_status = next_page(content,op_status)

    # Dict to list
    mylist = []
    for key, value in op_status.items():
        temp = [key,value]
        mylist.append(temp)

    rows = len(mylist)+5
    # Upload to Sheets
    try:
        worksheet = base.wks.add_worksheet(title="Ops By Status", rows=str(rows), cols="10")
    except APIError:
        worksheet = base.wks.worksheet("Ops By Status")

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # Label
    worksheet.update_acell('A2','Operation')
    worksheet.update_acell('B2','Status')
    worksheet.update_acell('C2','Last Modified')

    # Select a range
    org_list = worksheet.range('A3:A'+str(len(op_status)+2))
    status_list = worksheet.range('B3:B'+str(len(op_status)+2))
    changed_list = worksheet.range('C3:C'+str(len(op_status)+2))

    # Update organization
    index = 0
    for cell in org_list:
        cell.value = mylist[index][0]
        index+=1

    # Update status
    index = 0
    for cell in status_list:
        cell.value = mylist[index][1][0]
        index+=1

    # Update time changed
    index = 0
    for cell in changed_list:
        cell.value = mylist[index][1][1]
        index+=1

    # Update in batch (to avoid API timeout)
    worksheet.update_cells(org_list)
    worksheet.update_cells(status_list)
    worksheet.update_cells(changed_list)

if __name__ == '__main__':
    url = 'https://www.humanitarianresponse.info/api/v1.0/operations?fields=id,label,status,changed'
    ops_by_status(url)