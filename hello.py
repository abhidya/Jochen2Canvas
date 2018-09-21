import sys

sys.setrecursionlimit(5000)
import datetime
import requests
from requests import Session
from robobrowser import RoboBrowser
import configparser




#Constructing data on infectivity from website
args = sys.argv[1]
arglist = args.split()        #turn the args string into list items
username = str(arglist[0])        #number of bins
password = str(arglist[1])   #number of functions
val2 = str(arglist[2])     #numver of samples
val1 = str(arglist[3])     #numver of samples



#config = configparser.ConfigParser()
#config.read("config.ini")
#username = config.get("information", "Username")
#password = config.get("information", "Password")
#val2 = config.get("information", "Link-to-Personal-Site")
#val1 = config.get("information", "Canvas-Auth")

print('\n' + val1 + " " + val2)

calendar_link = "https://utk.instructure.com/api/v1/calendar_events?start_date=2018-05-02T04:00:00.000Z&end_date=2019-10-07T04:00:00.000Z&per_page=100&access_token="


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


requests.packages.urllib3.disable_warnings()
c = Session()
c.verify = False

browser = RoboBrowser(session=c, parser='html.parser')

browser.open('https://cas.tennessee.edu/cas/login?service=https%3A%2F%2Futk.instructure.com%2Flogin%2Fcas')
form = browser.get_form()
form['username'] = username
form['password'] = password
browser.submit_form(form)
poop = browser.find('body')
poop = str(poop['class'])
poop = find_between(poop, "'context-", "', 'lato-font-not-loaded-yet']")
print(poop)
user = poop

personal_site = val2
Canvas_authcode = val1
headers = {
    'Authorization': 'Bearer ' + Canvas_authcode}

browser.open(personal_site)
hrs = browser.find("body")

#
flag = False
day = ""
for list in hrs:
    list = str(list.encode('utf-8'))

    if (flag):
        if (r"b'\n'" != list):
            day = day.replace(r"""b'<b>\n""", "")
            day = day.replace(r": </b>'", "")
            day = day + str(" 2018")
            list = list.replace(r"b' \n", "")
            list = list.replace(r"\n'", "")
            list = list.replace(r"b'", '')
            list = list.replace(r'b"', '')
            list = list.replace(r"\n", ' ')
            list = list.lstrip()
            list = list.rstrip()
            manny_date = datetime.datetime.strptime(day, "%a %b %d %Y").strftime("%Y-%m-%d")
            print(manny_date + '\n' + list + '\n')
            check = c.get(calendar_link + val1, headers=headers)

            check = str(check.json())
            # print(list)
            if list not in check:
                # print(manny_date)
                fun = manny_date + 'T21:00:00Z'
                files = {
                    'calendar_event[context_code]': (None, user),
                    'calendar_event[title]': (None, list),
                    'calendar_event[start_at]': (None, fun),
                    'calendar_event[end_at]': (None, fun),
                    'calendar_event[description]': (None, '''<a href="''' + val2 + '''">Jochen's Hell Hole</a>''')
                }
                response = c.post('https://utk.instructure.com/api/v1/calendar_events.json', headers=headers, files=files)
                response = response.json()
                if "errors" in response:
                    print(response)
            else:
                print('\n' + "Assignment ALREADY ADDED, SKIPPING" + '\n')
        flag = False
    if ("<b>" in list):
        day = list
        flag = True
