# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# #1. List of all available routes starting at the homepage.
@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes for Hawaii: <br/>"
        f"Precipitation for the previous year: /api/v1.0/precipitation<br/>"
        f"Weather Stations available: /api/v1.0/stations<br/>"
        f"Daily temperatures in the previous year for Station USC00519281: /api/v1.0/tobs<br/>"
        f"/api/v1.0/Starting_Year(YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_ending_year(YYYY-MM-DD/YYYY-MM-DD)"
    )



#2. Last 12 months query results for the precipitation analysis
# Query added to a dictionary with KEY = Date and VALUE = Prcp 
# The JSON representation of this dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """query results from precipitation analysis"""
    # Query all precipitation
    prcp_end = dt.date(2017, 8, 23)
    prcp_12mo = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prcp_query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prcp_12mo).all()
    prcp_dictionary = dict(prcp_query)

    print(f"The precipitaion from {prcp_12mo} to {prcp_12mo} are {prcp_dictionary}")
    return jsonify(prcp_dictionary) 

    session.close()



#3. The JSON list of stations from the dataset


@app.route("/api/v1.0/stations")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    station_query = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    # Dictionary from the row data to append to a list of stations
    station_list = []
    for station, name, lat, lng, elevation in station_query:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = lat
        station_dict["Longitude"] = lng
        station_dict["Elevation"] = elevation
        station_list.append(station_dict)

    session.close()

    return jsonify(station_list)


#4. Dates and temperature observations Query of the most-active station for the previous year of data.
# JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)

     tobs_query = session.query(measurement.date, measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>='2016-08-23').all()

    ###### session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=prcp_12mo).all()

     tobs_list = []
     for date, tobs in tobs_query:
         tobs_dict = {}
         tobs_dict["Date"] = date
         tobs_dict["Tobs"] = tobs
         tobs_list.append(tobs_dict)

     return jsonify(tobs_list)


#5. JSON list of the minimum, maximmum and average temperature of the given date range.
#   Calculated Tmin, Tmax and Tavg for all the dates greater than or equal to the start date.
#   Calculated Tmin, Tmax and Tavg for the dates from the start date to the end date, inclusive.



@app.route("/api/v1.0/Starting_Year(YYYY-MM-DD)")

def Temp_start(start):
    session = Session(engine)
    start_temp_query = session.query(func.min(measurement.tobs),\
                                     func.max(measurement.tobs),\
                                     func.avg(measurement.tobs))\
                                     .filter(measurement.date >= start).all()
    session.close()

    temp_list = []
    for min_temp, max_temp, avg_temp in start_temp_query:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min_temp
        temp_dict['Maximum Temperature'] = max_temp
        temp_dict['Average Temperature'] = avg_temp
        temp_list.append(temp_dict)

    return jsonify(temp_list)


@app.route("/api/v1.0/start_ending_year(YYYY-MM-DD/YYYY-MM-DD)")
def Temp_start_end(start, end):
    session = Session(engine)
    start_end_temp_query = session.query(func.min(measurement.tobs),\
                                         func.max(measurement.tobs),\
                                         func.avg(measurement.tobs))\
                                         .filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    temp_list = []
    for min_temp, max_temp, avg_temp in start_end_temp_query:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min_temp
        temp_dict['Maximum Temperature'] = max_temp
        temp_dict['Average Temperature'] = avg_temp
        temp_list.append(temp_dict)

    return jsonify(temp_list)

