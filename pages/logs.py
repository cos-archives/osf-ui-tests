import datetime as dt
from collections import namedtuple

Log = namedtuple('Log', ['text', 'date', 'links'])

Link = namedtuple('Link', ['text', 'url'])


def parse_log(container):
    dates = container.find_elements_by_css_selector('dt')
    logs = container.find_elements_by_css_selector('dd')

    log_list = []

    for d, t in zip(dates, logs):
        log_list.append(
            Log(
                text=t.text,

                date=dt.datetime.strptime(
                    d.text.replace('1913', '2013', 1)[:-6], # includes temporary fix to year 1913 bug
                    '%m/%d/%Y %I:%M %p',
                ) - dt.timedelta(hours=int(d.text[-5:-2])),
                links=[Link(
                    text=lk.text,
                    url=lk.get_attribute('href'),
                ) for lk in t.find_elements_by_css_selector('a')]
            )
        )

    return log_list