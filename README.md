KML Parser
=====================


a group of scripts to manipulate **KML**[^gfm] files, generate elevation data or reversed coordinates



####reversekml.py

> **USAGE:**
>usage: reversekml.py [-h] [-v] kmz_file[^gfme] 
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

####parsekml.py

> **USAGE:**
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
./parsekml.py -v test.kmz tag
```

[^gfm]: **Keyhole Markup Language** (KML) is an XML notation for expressing geographic annotation and visualization within Internet-based, two-dimensional maps and three-dimensional Earth browsers.

[^gfme]: **KMZ** is Keyhole Markup Language files when compressed.
