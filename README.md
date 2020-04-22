# carbon-credentials-developer-test

## Interface
The interface is controlled by a menu on the left enabling the three sections of the assignment:

* Upload Data - to enable uploading the three types of .csv file to the database
* Explore Data - screens to navigate through the hierarchy of buildings, meters and readings
* Visualise Data - to view graphs to gain insight into the data


## Installation
From the carbon-credentials-developer-test directory, run the following to build a vitualenv and install requirements.
```bash
pip install virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run migrations:
```bash
make init
```

To run tests:
```bash
make test
```

To run django server:
```bash
make run
```
This is then accessible from your browser at http://127.0.0.1:8000/


## Design Decisions
An overview of the decisions made and options considered

### Models
The data has a clear heirarchy of Buildings -> Meters -> Meter Readings which naturally split into Building, Meter and MeterReading models with foreign keys mapping up the heirarchy.

I broke the meter fuel into it's own Fuel model to reduce duplicate data in the database and retain the relationship between fuel type and unit. It also enables addition fuel types to be added.

The tricky decision was how to store the Meter Readings. I considered three options, eventually settling on the first.

#### Store data using datetime provided
The spec make a point out of the data being stored in half-hour buckets. This method means the times are less structured but the data more flexible to other time intervals in the future.

Pros:
* Data easily added to without being locked into half hour time slots

Cons:
* Potentially makes querying and aggregation harder as dates and times are less structured that other solutions

#### Store data in Half Hour time intervals
This closely fits the data we've been provided.

Pros:
* Comparing data across different meters would be easy as the data is guarenteed to be locked into the same structure.

Cons:
* Hard to change or adapt in the future.

#### Store datetime splitting date and time
Another consideration ...

Pros:
* Calculating daily aggregations becomes easier

Cons:
* Hard to sort and compare times and time and data are split

### CSV Uploader
I built the csv uploader into its own module to help house the functionality in one place and keep the views simplified.

Given the similarities between parsing the csv files and saving them to their respective models, I considered building a CSVUploader in the Factory design pattern. This would make the module easily expandable by adding new factory classes for new CSV types.

Given more time, I would implement far better CSV validation. At the moment there is very little. Modularising this or looking at 3rd party libraries should make this simple and the code more robust taking into account that we are dealing with external data that could be badly formatted.
