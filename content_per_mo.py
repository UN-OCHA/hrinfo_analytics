'''
Outputs the number of documents/events/assessments/infographics uploaded in a given month/time period.
Based on content creation date on HR.info (NOT publication date).

Python IDE setup not needed - Run manually:
1) http://jupyter.org/try - Click "Try Jupyter with Python"
2) Wait as it sets up, then click the scissors icon (in the bar) 3 times
3) Copy and paste this script into the box, then hit run.
4) Enter requested information (start of time period, end of time period - exclusive, content type).
    Ex: 01/05/2018, 01/06/2018, documents - will give you the number of documents uploaded in May
    Note: if you scroll up, to the left of the box you will see "In []". If there is a "*" inside the brackets,
    that means the code is running. If there is a number in the brackets, the job has completed.
'''
import datetime
import calendar
import urllib.request
import json

def open_url(url):
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    content = json.loads(r.decode('utf-8'))
    return content

def next_page(content, count, END):
    try:
        url = content['next']['href']
        content, count, END = content_count(url, count, END)
    except KeyError:
        pass
    return content, count, END

def content_count(url, count, END):
    content = open_url(url)
    for entry in content['data']:
        time = int(entry['created'])
        if time >= END:
            return content, count, END
        count+=1
    content, count, END = next_page(content, count, END)
    return content, count, END

def main():
    START = input("Enter beginning of time period (DD/MM/YYYY): ")
    START = str(calendar.timegm(datetime.datetime.strptime(START, "%d/%m/%Y").timetuple()))
    END = input("Enter end of time period, exclusive (DD/MM/YYYY): ")
    END = int(calendar.timegm(datetime.datetime.strptime(END, "%d/%m/%Y").timetuple()))
    CONTENT = input("Enter content type (documents, events, infographics, assessments): ")

    url ='https://www.humanitarianresponse.info/en/api/v1.0/' \
         + CONTENT + '?filter[created][value]=' \
            + START +'&filter[created][operator]=">="&fields=created,label&sort=created'

    count = 0
    content, count, END = content_count(url, count, END)
    print(count)

if __name__ == '__main__':
    main()