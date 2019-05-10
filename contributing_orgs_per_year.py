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
            print(url)
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

def update_worksheet_year(years, year, range, worksheet):
    orgs = years[year]
    orgs = sorted(orgs, key=str.lower)
    num_orgs = str(len(years[year])+2)
    org_cells = worksheet.range(range + num_orgs)
    index = 0
    for cell in org_cells: #update orgs
        cell.value = orgs[index]
        index+=1
    worksheet.update_cells(org_cells)

def contribs_by_year():

    years = {}

    # current year
    utc = timezone('UTC')
    tstamp = int(datetime(2019, 1, 1, 0, 0, 0, tzinfo=utc).timestamp())
    tstamp = str(tstamp)

    # events
    events_url = 'https://www.humanitarianresponse.info/en/api/v1.0/events?fields=organizations.label,created&filter[created][value]=' + tstamp + '&filter[created][operator]=>='
    content = base.open_url(events_url)
    years = work(content,years)
    years = next_page(content,years)

    # docs
    docs_url = 'https://www.humanitarianresponse.info/api/v1.0/documents?fields=organizations.label,created&filter[created][value]=' + tstamp + '&filter[created][operator]=>='
    content = base.open_url(docs_url)
    years = work(content,years)
    years = next_page(content,years)

    # maps/infographics
    maps_url = 'https://www.humanitarianresponse.info/api/v1.0/infographics?fields=organizations.label,created&filter[created][value]=' + tstamp + '&filter[created][operator]=>='
    content = base.open_url(maps_url)
    years = work(content,years)
    years = next_page(content,years)

    spreadsheet = base.get_spreadsheet()
    try:
        worksheet = spreadsheet.add_worksheet(title="Contributing Orgs By Year", rows=100, cols=10)
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
        worksheet = spreadsheet.worksheet("Contributing Orgs By Year")

    # Pull time of program execution and update
    geneva = timezone('Etc/GMT-2')
    current_time = datetime.now(geneva)
    formatted_time = current_time.strftime("%d %m %Y %H:%M:%S")
    updated = "Sheet Last Updated: " + formatted_time + ' (GMT+2)'
    worksheet.update_acell('A1', updated)

    # 2012
    #update_worksheet_year(years, '2012', 'A3:A', worksheet)

    # 2013
    #update_worksheet_year(years, '2013', 'B3:B', worksheet)

    # 2014
    #update_worksheet_year(years, '2014', 'C3:C', worksheet)

    # 2015
    #update_worksheet_year(years, '2015', 'D3:D', worksheet)

    # 2016
    #update_worksheet_year(years, '2016', 'E3:E', worksheet)

    # 2017
    #update_worksheet_year(years, '2017', 'F3:F', worksheet)

    # 2018
    #update_worksheet_year(years, '2018', 'G3:G', worksheet)

    # 2019
    update_worksheet_year(years, '2019', 'H3:H', worksheet)

def main():
    contribs_by_year()

if __name__ == '__main__':
    main()
