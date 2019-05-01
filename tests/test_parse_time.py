import unittest
from ftpparser import parse_time
import datetime

DATE_OF_TEST = datetime.datetime(year=2000, month=6, day=1, tzinfo=datetime.timezone.utc)

TEST_TIMES = {
    #This year:
    'Jan 29 03:26': datetime.datetime(month=1, day=29, year=2000, hour=3, minute=26, tzinfo=datetime.timezone.utc),
    #Last year, as we're testing in June:
    'Dec 25 08:44': datetime.datetime(month=12, day=25, year=1999, hour=8, minute=44, tzinfo=datetime.timezone.utc),
    #Tests with years:
    'Apr  8  1994': datetime.datetime(month=4, day=8, year=1994, hour=0, minute=0, tzinfo=datetime.timezone.utc),
    'Feb 22  2001': datetime.datetime(month=2, day=22, year=2001, hour=0, minute=0, tzinfo=datetime.timezone.utc),
    '30-DEC-1996 17:44': datetime.datetime(month=12, day=30, year=1996, hour=17, minute=44, tzinfo=datetime.timezone.utc),
    '8-SEP-1996 16:09': datetime.datetime(month=9, day=8, year=1996, hour=16, minute=9, tzinfo=datetime.timezone.utc),
    '8-SEP-2018 16:09': datetime.datetime(month=9, day=8, year=2018, hour=16, minute=9, tzinfo=datetime.timezone.utc),
    '04-27-00  09:09PM': datetime.datetime(month=4, day=27, year=2000, hour=21, minute=9, tzinfo=datetime.timezone.utc),
    '04-27-97  12:09PM': datetime.datetime(month=4, day=27, year=1997, hour=12, minute=9, tzinfo=datetime.timezone.utc),
    '04-27-18  09:09AM': datetime.datetime(month=4, day=27, year=2018, hour=9, minute=9, tzinfo=datetime.timezone.utc)
}

class TestTime(unittest.TestCase):

    def test_parsetimes(self):
        for line, dt in TEST_TIMES.items():
            output = parse_time.parse_time(line, now=DATE_OF_TEST)
            self.assertEqual(dt, output, 'Invalid response for: %s' % line)
    