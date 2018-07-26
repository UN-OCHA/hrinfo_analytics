'''
Pull spaces and last modified
'''
import base
import time
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

    try:
        worksheet = base.wks.add_worksheet(title="Global Spaces", rows=len(spaces)+10, cols="5")
    except APIError:
        worksheet = base.wks.worksheet("Global Spaces")

    # label
    worksheet.update_acell('A1','Space')
    worksheet.update_acell('B1','Last Modified')

    # Select a range
    space_list = worksheet.range('A2:A'+str(len(spaces)+1))
    time_list = worksheet.range('B2:B'+str(len(times)+1))

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
