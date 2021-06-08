import icalendar
from app import account as acc

def to_ical(sco: int):
    time_slots = acc.get_account_reservations(sco)

    cal = icalendar.Calendar()
    cal.add('method', 'PUBLISH')
    cal.add('version', '2.0')
    cal.add('prodid', '-//romanpeters.nl//Olympos//NL')
    cal.add('tzid', 'Europe/Amsterdam')
    cal.add('calscale', 'GREGORIAN')

    for ts in time_slots:
        event = icalendar.Event()
        event.add('summary', ts.title)
        event.add('dtstart', ts.start_time)
        event.add('dtend', ts.end_time)
        event.add('location', "Sportcentrum Olympos, Uppsalalaan 3, 3584 CT UTRECHT")
        event.add('url', 'https://olympos.romanpeters.nl')
        cal.add_component(event)

    path = f'data/{sco}.ics'
    with open(path, 'wb') as f:
        f.write(cal.to_ical())

    return path