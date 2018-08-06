'''
Pulls contributing organizations (based on documents, events, maps/infographics) for each year  - automated
'''
import base
from gspread.exceptions import APIError
import time
import urllib.request
from datetime import datetime
from pytz import timezone

def next_page(content,years):
    try:
        try:
            url = content['next']['href']
            content = base.open_url(url)
            years = work(content, years)
            years = next_page(content, years)
        except KeyError:
            pass
    except urllib.request.HTTPError:
        try:
            url = content['next']['href']
            print(url)
            content = base.open_url(url)
            years = work(content, years)
            years = next_page(content, years)
        except KeyError:
            pass
    return years

def work(content, years):
    for event in content['data']:
        try:
            # grab the year
            year = int(event['created'])
            year = time.strftime("%Y", time.localtime(year))
            years.setdefault(year, [])

            # grab the organization(s)
            for org in event['organizations']:
                name = org['label']
                if name not in years[year]:
                    years[year].append(name)
                else:
                    continue
        except:
            pass # no year or no org
    return years

def contribs_by_year():

    years = {}

    # events
    events_url = 'https://www.humanitarianresponse.info/en/api/v1.0/events?fields=organizations.label,created'
    content = base.open_url(events_url)
    years = work(content,years)
    years = next_page(content,years)

    # docs
    docs_url = 'https://www.humanitarianresponse.info/api/v1.0/documents?fields=organizations.label,created'
    content = base.open_url(docs_url)
    years = work(content,years)
    years = next_page(content,years)

    # maps/infographics
    maps_url = 'https://www.humanitarianresponse.info/api/v1.0/infographics?fields=organizations.label,created'
    content = base.open_url(maps_url)
    years = work(content,years)
    years = next_page(content,years)

    try:
        worksheet = base.wks.add_worksheet(title="Contributing Orgs By Year", rows=100, cols=10)
        # label
        worksheet.update_acell('A2','2012')
        worksheet.update_acell('B2','2013')
        worksheet.update_acell('C2','2014')
        worksheet.update_acell('D2','2015')
        worksheet.update_acell('E2','2016')
        worksheet.update_acell('F2','2017')
        worksheet.update_acell('G2','2018')
        worksheet.update_acell('H2','2019')
    except APIError:
        worksheet = base.wks.worksheet("Contributing Orgs By Year")

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # 2012
    orgs = years['2012']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2012'])+2)
    org_cells = worksheet.range('A3:A'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2013
    orgs = years['2013']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2013'])+2)
    org_cells = worksheet.range('B3:B'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2014
    orgs = years['2014']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2014'])+2)
    org_cells = worksheet.range('C3:C'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2015
    orgs = years['2015']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2015'])+2)
    org_cells = worksheet.range('D3:D'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2016
    orgs = years['2016']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2016'])+2)
    org_cells = worksheet.range('E3:E'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2017
    orgs = years['2017']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2017'])+2)
    org_cells = worksheet.range('F3:F'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2018
    orgs = years['2018']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2018'])+2)
    org_cells = worksheet.range('G3:G'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

    # 2019
    orgs = years['2019']
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years['2019'])+2)
    org_cells = worksheet.range('H3:H'+num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

def main():
    contribs_by_year()

if __name__ == '__main__':
    main()
