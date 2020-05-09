# meter-data-visualiser

## Interface
The interface is controlled by a menu on the left enabling the three sections of the assignment:

* Upload Data - to enable uploading the three types of .csv file to the database
* Explore Data - screens to navigate through the hierarchy of buildings, meters and readings
* Visualise Data - to view graphs to gain insight into the data


## Installation
From the meter-data-visualiser directory, run the following to build a vitualenv and install requirements.
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

__Pros__:
* Data easily added to without being locked into half hour time slots

__Cons__:
* Potentially makes querying and aggregation harder as dates and times are less structured that other solutions

#### Store data in Half Hour time intervals
This closely fits the data we've been provided.

__Pros__:
* Comparing data across different meters would be easy as the data is guarenteed to be locked into the same structure.

__Cons__:
* Hard to change or adapt in the future.

#### Store datetime splitting date and time
Another consideration ...

__Pros__:
* Calculating daily aggregations becomes easier

__Cons__:
* Hard to sort and compare times and time and data are split

### CSV Uploader
I built the csv uploader into its own module to help house the functionality in one place and keep the views simplified.

Given the similarities between parsing the csv files and saving them to their respective models, I considered building a CSVUploader in the Factory design pattern. This would make the module easily expandable by adding new factory classes for new CSV types.

Given more time, I would implement far better CSV validation. At the moment there is very little. Modularising this or looking at 3rd party libraries should make this simple and the code more robust taking into account that we are dealing with external data that could be badly formatted.

### Visualisation
I considered a number of graphing tools that play nicely with Django. I decided on [django-jchart](https://github.com/matthisk/django-jchart) which acts as a django wrapper around [Chartjs](https://www.chartjs.org/).

It comes with a lot for free and a fairly simple class based design for building the chart data.

## Improvements
If I had more time there are a number of areas I would improve and implement:
1. More testing. There are large gaps in testing but I have tried to demonstrate a range of test cases.
2. Logging - there currently isn't any.
3. Error handling - particularly around the CSV importing. Right now, it is very brittle and doesn't give good feedback to the user when it is unable to parse. Also, entries that invalidate foreign keys or don't pass the basic validation just get ignored. It would be good to feed this back to the user.
4. More visualisations. I was planning to agreggate data to monthly and compare with previous years as shown the example, adding date ranges when generating graphs. Also, plotting two meters on the same graph for comparison.
5. Import csv in chunks. The readings file is large and currently reading the whole file into memory is very resource intensive. Django provides file 'chunking' on its InMemoryUploadFile. Large files could also be processed in a background task rather than in the view.
