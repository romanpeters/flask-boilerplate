import time
import requests
import app.database as db
import app.olympos as oly
from app.feed import to_ical


def validate_sco(sco):
    url = f"https://olympos.nl/Inloggen/tabid/422/ctl/Bestaand/mid/896/language/nl-NL/Default.aspx?s=SCO{sco}"
    page = requests.get(url)
    if page.status_code == 200:
        return True

def get_account_reservations(sco) -> list:  # from db
    session = db.Session()
    reservations = session.query(db.Reservations).filter_by(user_id=sco).all()
    result = []
    for r in reservations:
        entry = session.query(db.TimeSlots).filter_by(ts_id=r.ts_id).first()
        if entry:
            result.append(oly.db_ts_to_dc_ts(entry))
    session.close()
    return result


class User(object):
    def __init__(self, sco: int, pwd: str):
        self.sco: int = sco
        self.pwd: str = pwd

        self.first_name: str = str()
        self.last_name: str = str()
        self.cookies: list = []
        self.reservation_page = None
        self.reservations: list = []

        self.db = UserDatabaseConnection(self)

        entry = self.db.get_db_user_entry()

        if entry:  # is existing user
            self.first_name = entry.first_name
            self.last_name = entry.last_name
            self.cookies = eval(entry.cookies) if entry.cookies else []  # <--

        self.cookie_is_valid: bool = self.check_cookie()
        if not self.cookie_is_valid:
            self.cookies = []

        self.login_is_valid: bool = True if self.cookie_is_valid else False
        self.login_is_valid = self.update()

        if not entry:
            self._add_name()
            # add to db


    def check_cookie(self) -> bool:
        if not self.cookies:
            return False
        dotnetnuke = [c for c in self.cookies if c['name'] == '.DOTNETNUKE'][0]
        print(f"it's {int(time.time())}, expires at {dotnetnuke['expiry']}")
        if int(dotnetnuke['expiry']) > time.time():
            print("Cookie is still fresh")
            return True
        else:
            print("Cookie is no longer fresh")
            return False

    def update(self) -> bool:
        """
        Checks login through Elemental
        Takes time
        Sets fresh cookies
        Sets self.reservation_page
        creates .ical
        """
        if not self.cookies:
            reservation_page = oly.Reservations(sco=self.sco, pwd=self.pwd)
        else:
            reservation_page = oly.Reservations(cookies=self.cookies)

        if reservation_page.page.status_code == 200:
            self.reservation_page = reservation_page
            self.db.add_reservations_to_db()
            self.cookies = self.reservation_page.cookies
            print('updated')
            return True
        print('update failed')
        return False

    def _add_name(self):
        info_page = oly.MyInfo(cookies=self.cookies)
        self.first_name = info_page.data['voornaam']
        self.last_name = ' '.join([info_page.data['tussenvoegsel'], info_page.data['achternaam']]).strip()


class UserDatabaseConnection(object):
    def __init__(self, user):
        self.user = user

    def add_user_to_db(self) -> bool:
        session = db.Session()
        session.merge(db.Users(user_id=self.user.sco, password=self.user.pwd, cookies=str(self.user.cookies),
                               first_name=self.user.first_name, last_name=self.user.last_name))
        return session.commit()

    def add_reservations_to_db(self) -> bool:
        print('adding reservations to the db')
        session = db.Session()
        for ts in self.user.reservation_page.items:
            print(ts.ts_id)
            reservation_id = ''.join([str(self.user.sco), ts.ts_id])
            if not ts.is_cancelled:
                reservation = db.Reservations(reservation_id=reservation_id, ts_id=ts.ts_id, user_id=self.user.sco)
                time_slot = db.TimeSlots(ts_id=ts.ts_id, title=ts.title,
                                         start_time=ts.start_time, end_time=ts.end_time)
                session.merge(reservation)
                session.merge(time_slot)
            else:
                entry = session.query(db.Reservations).filter_by(reservation_id=reservation_id).first()
                if entry:
                    session.delete(entry)
        return session.commit()

    def get_db_user_entry(self) -> db.Users:
        session = db.Session()
        entry = session.query(db.Users).filter_by(user_id=self.user.sco).first()
        session.close()
        return entry

    def get_db_reservations(self) -> list:
        entries = []
        session = db.Session()
        reservations = session.query(db.Reservations).filter_by(user_id=self.user.sco).all()
        for r in reservations:
            entry = session.query(db.TimeSlots).filter_by(ts_id=r.ts_id).first()
            if entry:
                entries.append(entry)
        session.close()

        return [oly.db_ts_to_dc_ts(e) for e in entries]  # convert to dataclass