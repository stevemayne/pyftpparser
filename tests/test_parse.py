#name, size, _sizetype, mtime, _mtimetype, cwd, retr, _id, _idtype, islink

import unittest
from ftp_parser import parse
import datetime

DATE_OF_TEST = datetime.datetime(year=2000, month=6, day=1)

TEST_CASES = [ \
    # ELPF - see http://pobox.com/~djb/proto/eplf.txt
    ('+i8388621.29609,m824255902,/,\tdev',
        [('dev', 0, 824255902, 1, 0, 0, None)]),
    ('+i8388621.44468,m839956783,r,s10376,\tRFCEPLF',
        [('RFCEPLF', 10376, 839956783, 0, 1, 0, None)]),
    # UNIX-style listing, without inum and without blocks
    # UNIX ls does not show the year for dates in the last six months.
    ('-rw-r--r--   1 root     other        531 Jan 29 03:26 README',
     [('README', 531, int(datetime.datetime(month=1, day=29, year=2000, hour=3, minute=26, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, 'rw-r--r--')]),
    ('dr-xr-xr-x   2 root     other        512 Apr  8  1994 etc',
        [('etc', 512, 765763200, 1, 0, 0, 'r-xr-xr-x')]),
    ('dr-xr-xr-x   2 root     512 Apr  8  1994 etc',
        [('etc', 512, 765763200, 1, 0, 0, 'r-xr-xr-x')]),
    ('-r-xr-xr-x   1 root  wheel  3258128 Nov 20  2000 kernel.GENERIC',
        [('kernel.GENERIC', 3258128, 974678400, 0, 1, 0, 'r-xr-xr-x')]),
    ('lrwxrwxrwx   1 root  wheel       11 Feb 22  2001 sys -> usr/src/sys',
        [('sys', 11, 982800000, 1, 1, 1, 'rwxrwxrwx')]),
    ('drwxr-xr-x   2 root  wheel      512 Feb 22  2001 cdrom',
        [('cdrom', 512, 982800000, 1, 0, 0, 'rwxr-xr-x')]),
    ('lrwxrwxrwx   1 root     other          7 Jan 25 00:17 bin -> usr/bin',
     [('bin', 7, int(datetime.datetime(month=1, day=25, year=2000, hour=0, minute=17, tzinfo=datetime.timezone.utc).timestamp()), 1, 1, 1, 'rwxrwxrwx')]),
    ('-rw-r-----  1 md  staff  13500 Dec 25 08:44 ftpparse.c',
     [('ftpparse.c', 13500, int(datetime.datetime(month=12, day=25, year=1999, hour=8, minute=44, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, 'rw-r-----')]),
    # Also produced by Microsoft's FTP servers for Windows:
    ('----------   1 owner    group         1803128 Jul 10 10:18 ls-lR.Z',
     [('ls-lR.Z', 1803128, int(datetime.datetime(month=7, day=10, year=1999, hour=10, minute=18, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, '---------')]),
    ('d---------   1 owner    group               0 May  9 19:45 Softlib',
     [('Softlib', 0, int(datetime.datetime(month=5, day=9, year=2000, hour=19, minute=45, tzinfo=datetime.timezone.utc).timestamp()), 1, 0, 0, '---------')]),
    # Also WFTPD for MSDOS:
    ('-rwxrwxrwx   1 noone    nogroup      322 Aug 19  1996 message.ftp',
        [('message.ftp', 322, int(datetime.datetime(month=8, day=19, year=1996, hour=0, minute=0, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, 'rwxrwxrwx')]),
    # Also NetWare:
    ('d [R----F--] supervisor            512       Jan 16 18:53    login',
     [('login', 512, int(datetime.datetime(month=1, day=16, year=2000, hour=18, minute=53, tzinfo=datetime.timezone.utc).timestamp()), 1, 0, 0, None)]),
    ('- [R----F--] rhesus             214059       Oct 20 15:27    cx.exe',
     [('cx.exe', 214059, int(datetime.datetime(month=10, day=20, year=1999, hour=15, minute=27, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, None)]),
    # Also NetPresenz for the Mac:
    ('-------r--         326  1391972  1392298 Nov 22  1995 MegaPhone.sit',
        [('MegaPhone.sit', 1392298, 816998400, 0, 1, 0, '------r--')]),
    ('drwxrwxr-x               folder        2 May 10  1996 network',
        [('network', 2, 831686400, 1, 0, 0, 'rwxrwxr-x')]),
    # MultiNet (some spaces removed from examples)
    ('00README.TXT;1      2 30-DEC-1996 17:44 [SYSTEM] (RWED,RWED,RE,RE)',
        [('00README.TXT', 0, 851967840, 0, 1, 0, None)]),
    ('CORE.DIR;1          1  8-SEP-1996 16:09 [SYSTEM] (RWE,RWE,RE,RE)',
        [('CORE', 0, 842198940, 1, 0, 0, None)]),
    # and non-MutliNet VMS:
    ('CII-MANUAL.TEX;1  213/216  29-JAN-1996 03:33:12  [ANONYMOU,ANONYMOUS]   (RWED,RWED,,)',
        [('CII-MANUAL.TEX', 0, int(datetime.datetime(month=1, day=29, year=1996, hour=3, minute=33, second=12, tzinfo=datetime.timezone.utc).timestamp()), 0, 1, 0, None)]),
    # MSDOS format
    ('04-27-00  09:09PM       <DIR>          licensed',
        [('licensed', 0, 956869740, 1, 0, 0, None)]),
    ('07-18-00  10:16AM       <DIR>          pub',
        [('pub', 0, 963915360, 1, 0, 0, None)]),
    ('04-14-00  03:47PM                  589 readme.htm',
        [('readme.htm', 589, 955727220, 0, 1, 0, None)]),
    # Some useless lines, safely ignored:
    ('Total of 11 Files, 10966 Blocks.',
        [None]),
    ('total 14786',
        [None]),
    ('DISK$ANONFTP:[ANONYMOUS]',
        [None]),
    ('Directory DISK$PCSA:[ANONYM]',
        [None])]

class TestParse(unittest.TestCase):

    def test_testknownvalues(self):
        parser = parse.FTPParser()
        for (question, answer) in TEST_CASES:
            result = parser.parse([question], now=DATE_OF_TEST)
            self.assertEqual(answer, result)