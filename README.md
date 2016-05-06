# geo-tools
A bunch of geoip tools.

- Author: major1201
- Current version: 0.1

## Summary

This tool is used to display geo info of hostnames and IPs.

## Usage

- lookup one or more hostnames and IP addresses in simple mode
```
$ python geo.py 8.8.8.8 208.67.220.220 www.python.org
8.8.8.8(8.8.8.8) - United States, California, Mountain View
208.67.220.220(208.67.220.220) - United States, California, San Francisco
www.python.org(23.235.43.223) - United States
```

- lookup one or more hostnames and IP addresses in detailed mode
```
$ python geo.py -d 8.8.8.8 www.python.org
8.8.8.8(8.8.8.8):
Country ISO code: 
Country name: United States
Subdivision ISO code: CA
Subdivision name: California
City name: Mountain View
Postal code: 94040
Latitude: 37.3845
Longitude: -122.0881
-
www.python.org(103.245.222.223):
Country ISO code: 
Country name: Australia
Subdivision ISO code: 
Subdivision name: 
City name: 
Postal code: 
Latitude: -27.0
Longitude: 133.0
```

- display result in another language
```
$ python geo.py dw.de -l de
dw.de(194.55.26.46) - Deutschland, Nordrhein-Westfalen, Bonn
dw.de(194.55.30.46) - Deutschland, Nordrhein-Westfalen, Troisdorf
```

- pipe a command to geo.py
```
traceroute www.google.com | python geo.py -f '%s %c'
traceroute to www.google.com (172.217.4.68), 30 hops max, 60 byte packets       California Mountain View
 1  45.55.128.253 (45.55.128.253)  0.716 ms  0.614 ms 45.55.128.254 (45.55.128.254)  0.550 ms   New York New York
 2  162.243.188.241 (162.243.188.241)  0.546 ms 162.243.188.229 (162.243.188.229)  0.516 ms  0.576 ms   New York New York
 3  162.243.188.250 (162.243.188.250)  0.561 ms  0.444 ms  0.423 ms     New York New York
 4  162.243.188.255 (162.243.188.255)  1.232 ms 216.239.50.108 (216.239.50.108)  1.604 ms 162.243.188.255 (162.243.188.255)  1.189 ms   New York New York
 5  209.85.240.113 (209.85.240.113)  1.654 ms  1.836 ms  2.010 ms       California Mountain View
 6  lga15s47-in-f4.1e100.net (172.217.4.68)  1.126 ms 209.85.240.113 (209.85.240.113)  1.657 ms  1.748 ms       California Mountain View
```

- you can see all usages using `-h` or `--help` option
```
$ python geo.py -h
```

## Requirements

- geoip2 `pip install geoip2`
- argparse `pip install argparse`

## License

This project follows GNU General Public License v3.0.
