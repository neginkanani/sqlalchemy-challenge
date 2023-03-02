This code do a climate analysis about the area. The following sections outline the steps :

Python is used to read a sqlite database

The most recent date in the dataset is found.

Using that date, the previous 12 months of precipitation data were found and plotted.

The most-active stations were found and the lowest, highest, and average temperatures for the most-active station were calculated.

The previous 12 months of temperature observation (TOBS) data were filtered and the results were plotted as a histogram with bins=12.

Finally a Flask API was designed based on the queries that were developed. 

("/")
 List all the available routes.

("/api/v1.0/precipitation")
Convert the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

("/api/v1.0/stations") Return a JSON list of stations from the dataset.

()"/api/v1.0/tobs")
Query the dates and temperature observations of the most-active station for the previous year of data.


("/api/v1.0/<start>" and "/api/v1.0/<start>/<end>")
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculates the TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculates TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


    

