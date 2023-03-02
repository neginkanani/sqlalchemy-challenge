import sqlite3 as sql
from flask import Flask, jsonify
# from itertools import chain
from datetime import datetime
import numpy as np
import pandas as pd
import datetime as dt


#Read the sqlite

with sql.connect("C:/Users/arupm/Desktop/bootcamp/Homeworks/sqlalchemy-challenge/Starter_Code/Resources/hawaii.sqlite") as con:
        cur = con.cursor()
        colnames_measurement=cur.execute("select * from measurement")
        rows_measurement = cur.fetchall()
        print(f"info of the measurement table {colnames_measurement.description} ")
        
        cur2 = con.cursor()
        colnames_station=cur2.execute("select * from station")
        rows_station = cur2.fetchall()
        print(f"info of the station table {colnames_station.description} ")
        

con.close()

#read the measurement table
df_dic=[]
for j in np.arange(len(rows_measurement)):
    temp={colnames_measurement.description[0][0]:rows_measurement[j][0],
    colnames_measurement.description[1][0]:rows_measurement[j][1],
    colnames_measurement.description[2][0]:rows_measurement[j][2],
    colnames_measurement.description[3][0]:rows_measurement[j][3],
    colnames_measurement.description[4][0]:rows_measurement[j][4]}
    df_dic.append(temp)
    
measurement=pd.DataFrame(df_dic)

#read the station table
df_dic=[]
for j in np.arange(len(rows_station)):
    temp={colnames_station.description[0][0]:rows_station[j][0],
    colnames_station.description[1][0]:rows_station[j][1],
    colnames_station.description[2][0]:rows_station[j][2],
    colnames_station.description[3][0]:rows_station[j][3],
    colnames_station.description[4][0]:rows_station[j][4],
    colnames_station.description[5][0]:rows_station[j][5]}
    df_dic.append(temp)
    
station=pd.DataFrame(df_dic)


# finding the last 12 months of data
measurement["Date"]=pd.to_datetime(measurement["date"])
most_recent_date = measurement.sort_values("Date", ascending=False)
recent_year=most_recent_date.iloc[[0],4]
Prev_Year= (most_recent_date.iloc[[0],5]- dt.timedelta(days=365))
last_12_months_temp=measurement[(measurement.loc[:,"Date"]>="2016-08-23") & (measurement.loc[:,"Date"]<="2017-08-23")]


#most active station
most_active_station=pd.DataFrame(measurement.groupby("station")["station"].count().sort_values(ascending=False)).\
rename(columns={"station":"count_station"}).reset_index()
most_active_station_name=most_active_station.loc[0,"station"]


app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# defining the availabe routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/2016-08-23<br>"
        f"/api/v1.0/2016-08-23/2017-08-23<br>"
        
    )


# # retrieves  the last 12 months of data to a dictionary using date as the key and prcp as the value
@app.route("/api/v1.0/precipitation")
def precipitation():

    last_12_months_dict={}

    station_list=['USC00519397', 'USC00513117', 'USC00514830', 'USC00517948','USC00518838', 'USC00519523', 'USC00519281', 'USC00511918','USC00516128']
    for s in station_list:
        temp=last_12_months_temp[last_12_months_temp["station"]==s]
        temp2=temp[["date","prcp"]].dropna().reset_index(drop=True).set_index("date")
        temp2_dict=temp2.to_dict()
        last_12_months_dict[s]=temp2_dict

    return jsonify(last_12_months_dict)

#Returns a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stationlistname():
    station_dict={}
    station_dict["station"]=list(station["station"])
    return jsonify(station_dict)

#Queries the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def temperature():
    activestation=last_12_months_temp[last_12_months_temp["station"]==most_active_station_name]
    activestation_dict=activestation[["date","tobs"]].set_index("date").to_dict()
    return jsonify(activestation_dict)


@app.route("/api/v1.0/<start>")
def temperatureSummary(start):
    temp_summary={}
    temp_summary["min_T"]=measurement[measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")]["tobs"].min()
    temp_summary["max_T"]= measurement[measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")]["tobs"].max()
    temp_summary["mean_T"]=measurement[measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")]["tobs"].mean()
    return jsonify(temp_summary)

# Queries for a specified start,  minTemp, avgtemp  and maxtemp for all the dates greater than or equal to the start date.
# ueries for a specified start and end date, minTemp, avgtemp  and maxtemp for the dates from the start date to the end date.
@app.route("/api/v1.0/<start>/<end>")
def temperatureSummary2(start, end):
    temp_summary2={}
    temp_summary2["min_T"]=(measurement[(measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")) & (measurement["Date"]<=dt.datetime.strptime(end, "%m-%d-%Y"))]["tobs"].min())
    temp_summary2["max_T"]= (measurement[(measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")) & (measurement["Date"]<=dt.datetime.strptime(end, "%m-%d-%Y"))]["tobs"].max())
    temp_summary2["mean_T"]=(measurement[(measurement["Date"]>=dt.datetime.strptime(start, "%m-%d-%Y")) & (measurement["Date"]<=dt.datetime.strptime(end, "%m-%d-%Y"))]["tobs"].mean())
    return jsonify(temp_summary2)

if __name__ == '__main__':
    app.run(debug=True)