from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import hashlib
import dateparser
from dataclasses import dataclass
import elemental


@dataclass
class FitnessTimeslot:
    ts_id: str
    title: str
    start_time: datetime
    end_time: datetime
    niveau: str = None
    maximum: int = None
    gereserveerd: int = None
    reserveringen: list = None
    available: bool = None
    is_cancelled: bool = False


def db_ts_to_dc_ts(entry):
    """database.TimeSlots() to olympos.FitnessTimeslot()"""
    dataclass = FitnessTimeslot(ts_id=entry.ts_id,
                                title=entry.title,
                                start_time=entry.start_time,
                                end_time=entry.end_time)
    return dataclass


class OlymposPage(object):
    url = "https://www.olympos.nl/"

    def __init__(self, cookies=None):
        self.time_slots: list = []
        session = requests.Session()
        if cookies:
            for c in cookies:
                session.cookies.set(name=c['name'], value=c['value'])
        print(f"reaching for {self.url} (cookies: {'yes' if cookies else 'no'})")
        self.page = session.get(self.url)
        if self.page.status_code != 200:
            print("olympos onbereikbaar")
        self.soup = BeautifulSoup(self.page.text, "html.parser")


    @staticmethod
    def hash_item(items: list):
        return hashlib.sha256(''.join([str(i) for i in items]).encode()).hexdigest()[:10]

    def _row2dataclass(self, row):
        raise NotImplementedError

    def _generate_ts(self):
        py_table = []
        result = []

        for row in self.html_table.findAll("tr"):
            new_row = []
            for cell in row.findAll("td"):
                clean_cell = cell.text.strip()
                if clean_cell:
                    new_row.append(clean_cell)
            py_table.append(new_row)

        for row in py_table[1:]:
            #if row[-1].lower() not in ['kan nu niet meer', 'volgeboekt']:
            result.append(self._row2dataclass(row))
        return result

    @property
    def items(self):
        return self.time_slots


class FitnessPage(OlymposPage):
    url = "https://www.olympos.nl/nl-nl/sportaanbod/groepslessen/allegroepslessen/details.aspx?sportgroep=FITNESS+C#Groepsles"

    def __init__(self, cookies=None):
        super().__init__(cookies)
        self.html_table = self.soup.find("table")
        self.time_slots: list = self._generate_ts()


    def _row2dataclass(self, row):
        start_time = dateparser.parse(f"{row[1]} {row[2].split()[0]}")
        title = 'Fitness vrij sporten'
        available = False if row[-1].lower() in ['kan nu niet meer', 'volgeboekt'] else True
        return FitnessTimeslot(ts_id=self.hash_item([start_time, title]),
                               title=title,
                               start_time=start_time,
                               end_time=dateparser.parse(f"{row[1]} {row[2].split()[-1]}"),
                               niveau=row[3],
                               maximum=row[4],
                               gereserveerd=row[5],
                               available=available
                               )



class Reservations(OlymposPage):
    url = "https://www.olympos.nl/nl-nl/mijnsportoverzicht.aspx"

    def __init__(self, sco=None, pwd=None, cookies=None):
        assert (sco and pwd) or cookies, "I need cookies, or sco+pwd"
        self.cookies = cookies
        self.sco = sco
        self.pwd = pwd
        if (sco and pwd) and not cookies:
            self.cookies: list = self.get_login_cookie(sco, pwd)
        super().__init__(self.cookies)
        self.html_table = self.soup.find("table")
        self.time_slots: list = self._generate_ts()

    def get_login_cookie(self, sco, pwd):
        print("using elemental")
        browser = elemental.Browser(headless=True)
        url = f"https://www.olympos.nl/Inloggen/tabid/422/ctl/Bestaand/mid/896/language/nl-NL/Default.aspx?s=SCO{sco}&returnurl=/nl-nl/home.aspx"
        browser.visit(url)
        browser.get_input(class_name="NormalTextBox wachtwoord").fill(pwd)
        browser.get_input(class_name="StandardButton verder").click()
        cookies = browser.selenium_webdriver.get_cookies()
        browser.quit()
        return [{str(k): str(v) for k, v in d.items()} for d in cookies]

    def _row2dataclass(self, row):
        start_time = dateparser.parse(row[0])
        title = row[1]
        return FitnessTimeslot(ts_id=self.hash_item([start_time, title]),
                               title=title,
                               start_time=dateparser.parse(row[0]),
                               end_time=start_time + timedelta(minutes=75),
                               is_cancelled=True if row[2] == 'Geannuleerd' else False)

class MyInfo(OlymposPage):
    url = "https://olympos.nl/nl-nl/mijngegevens.aspx"

    def __init__(self, cookies):
        assert cookies, 'cookies needed'
        print('gathering personal info')
        self.cookies = cookies
        super().__init__(self.cookies)
        self.html_table = self.soup.find("table")
        self.data: dict = self._get_info()

    def _get_info(self):
        result = dict()
        for row in self.html_table.findAll("tr"):
            key = row.findAll("td", {'class', 'label'})[0].text.strip().lower()
            value = row.findAll("td", {'class', 'waarde'})[0].text.strip()
            result[key] = value
        return result
