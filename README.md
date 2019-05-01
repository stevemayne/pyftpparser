ftpparser
---------

ftpparser is a Python 3 package for parsing FTP LIST results for a variety of FTP server formats

Install:

```bash
pip3 install ftpparser
```

Usage:

```python
import ftpparser

parser = ftpparser.FTPParser()
results = parser.parse(['-r-xr-xr-x   1 root  wheel  3258128 Nov 20  2019 kernel.GENERIC'])
name, size, timestamp, isdirectory, downloadable, islink, permissions = results[0]
```


