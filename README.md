# pygtfsdb
This is a quick project that loads GTFS Static (General Transit Feed Specification) data into a relational database. It is currently only tested with sqlite but is intended to later work more speicifically with postgresql + postgis.

TODO: Add parameter for enabling spatial data.
## Installation
At the moment you should just clone the repo to your project then run `pip -r requirements.txt`.
## Usage
### Load from url
```python
gt = GtfsDb('sqlite:///test.db')
gt.load("http://transitfeeds.com/p/bart/58/latest/download", "Bart")
```
### Load from local file
```python
zf = ZipFile(localfile)
gt.load(zf, "Bart")
```

