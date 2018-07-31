'''
Pulls documents counts for all organizations - automated
'''
import content_counts
import base

def counts(num_orgs, org_info, worksheet, rows):

    doc_counts = []
    docs_base_url = 'https://www.humanitarianresponse.info/en/api/v1.0/documents?fields=organizations.id&filter[organizations]='

    cell_num = 3
    for index in range(0, num_orgs):
        org_id = org_info[index][0]
        count = 0
        docs_full_url = docs_base_url + str(org_id)
        content = base.open_url(docs_full_url)
        count += len(content['data'])
        content,count = content_counts.next_page(content,count)
        doc_counts.append((org_id,count))
        cell_num+=1

    doc_cells = worksheet.range('B3:B'+rows)
    index = 0
    for cell in doc_cells:
        cell.value = doc_counts[index][1]
        index+=1
    worksheet.update_cells(doc_cells)

    updated = content_counts.update_timestamp(worksheet)
    worksheet.update_acell('B1', updated)

def main():
    num_orgs, org_info, worksheet, rows = content_counts.content()
    counts(num_orgs, org_info, worksheet, rows)

if __name__ == '__main__':
    main()
