KML Parser
=====================

A group of scripts to manipulate **KML** files, generate elevation data or reversed coordinates

####reversekml.py

> **USAGE:**
>
>usage: reversekml.py [-h] [-v] kmz_file
>
>KMZ reverse coordinates
>
>positional arguments:
>  kmz_file       the .kmz file
>
>optional arguments:
>  -h, --help     show this help message and exit
>  -v, --verbose

#####Example:
```
./reversekml.py -v test.kmz
```

####parsemaps.py

> **USAGE:**
>
>usage: reversekml.py [-h] [-v] kmz_file
>
>KMZ reverse coordinates
>
>positional arguments:
>  kmz_file       the .kmz file
>
>optional arguments:
>  -h, --help     show this help message and exit
>  -v, --verbose

#####Example:
```
./parsemaps.py -v test.kmz tag
```
