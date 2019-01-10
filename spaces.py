'''
Pull spaces and date/time last modified - automated
'''
import base
import time
from datetime import datetime
from pytz import timezone
from gspread.exceptions import APIError

def spaces(url):
    content = base.open_url(url)
    spaces = []
    times = []
    for data in content['data']:
        last_modified = int(data['changed'])
        last_modified = time.strftime("%Y %d %b", time.localtime(last_modified))
        spaces.append(data['label'])
        times.append(last_modified)

    spreadsheet = base.get_spreadsheet()
    try:
        worksheet = spreadsheet.add_worksheet(title="Global Spaces", rows=len(spaces)+10, cols="5")
    except APIError:
        worksheet = spreadsheet.worksheet("Global Spaces")

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # label
    worksheet.update_acell('A2','Space')
    worksheet.update_acell('B2','Last Modified')

    # Select a range
    space_list = worksheet.range('A3:A'+str(len(spaces)+2))
    time_list = worksheet.range('B3:B'+str(len(times)+2))

    index = 0
    for cell in space_list: #update id
        cell.value = spaces[index]
        index+=1

    index = 0
    for cell in time_list: #update names
        cell.value = times[index]
        index+=1

    # Update in batch - avoids API timeout problem
    worksheet.update_cells(space_list)
    worksheet.update_cells(time_list)

def main():
    url = 'https://www.humanitarianresponse.info/api/v1.0/spaces?fields=label,changed'
    spaces(url)

if __name__ == '__main__':
    main()
