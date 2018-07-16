'''
Lists operations by status, as well as the date each operation was last modified.
'''

import base
from gspread.exceptions import APIError
import time

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

    # Label
    worksheet.update_acell('A1','Operation')
    worksheet.update_acell('B1','Status')
    worksheet.update_acell('C1','Last Modified')

    # Select a range
    org_list = worksheet.range('A2:A'+str(len(op_status)+1))
    status_list = worksheet.range('B2:B'+str(len(op_status)+1))
    changed_list = worksheet.range('C2:C'+str(len(op_status)+1))

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