'''
Pulls map/infographic counts for all organizations - automated
'''
import content_counts
import base

def counts(num_orgs, org_info, worksheet, rows):

    map_counts = []
    maps_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/infographics?fields=organizations.id&filter[organizations]='

    cell_num = 3
    for index in range(0,num_orgs):
        org_id = org_info[index][0]
        count = 0
        maps_full_url = maps_base_url + str(org_id)
        content = base.open_url(maps_full_url)
        count += len(content['data'])
        content,count = content_counts.next_page(content,count)
        map_counts.append((org_id,count))
        cell_num+=1

    map_cells = worksheet.range('C3:C'+rows)
    index = 0
    for cell in map_cells:
        cell.value = map_counts[index][1]
        index+=1
    worksheet.update_cells(map_cells)

    updated = content_counts.update_timestamp(worksheet)
    worksheet.update_acell('C1', updated)

def main():
    num_orgs, org_info, worksheet, rows = content_counts.content()
    counts(num_orgs, org_info, worksheet, rows)

if __name__ == '__main__':
    main()