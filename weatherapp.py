import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, Column, Integer, String, desc, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine, reflect = True)

# Save reference to the table
Measures = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precip<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/enter_start_date (YYYY-MM-DD)<br/>"
        f"/api/v1.0/enter_start_date (YYYY-MM-DD)/enter_end_date (YYYY-MM-DD)"
    )

# Returns json with the date as the key and the value as the precipitation
# Only returns the jsonified precipitation data for the last year in the database

@app.route("/api/v1.0/precip")
def precip():
    session = Session(engine)

    # Find the most recent date in the data set.
    re_date = session.query(func.max(Measures.date)).scalar()

    # Calculate date from a year before most recent date
    year_ago = dt.datetime.strptime(re_date, '%Y-%m-%d') - dt.timedelta(days=366)


    results = session.query(Measures.date, Measures.prcp).filter(Measures.date >= year_ago)

    session.close()

    rain_year = []
    for dat, prec in results:
        rain_dict = {}
        rain_dict[dat] = prec
        rain_year.append(rain_dict)
    
    return jsonify(rain_year)






# Returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measures.station, func.count(Measures.station)).\
                group_by(Measures.station).order_by(desc(func.count(Measures.station))).all()

    session.close()

    all_stations = []
    for sta, cou in results:
        sta_dict = {}
        sta_dict[sta] = cou
        all_stations.append(sta_dict)
    
    return jsonify(all_stations)


# Returns jsonified data for the most active station (USC00519281)
# Only returns the jsonified data for the last year of data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Find the most recent date in the data set.
    re_date = session.query(func.max(Measures.date)).scalar()

    # Calculate date from a year before most recent date
    year_ago = dt.datetime.strptime(re_date, '%Y-%m-%d') - dt.timedelta(days=366)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # Listthe stations and the counts in descending order.
    unique_counts = session.query(Measures.station, func.count(Measures.station)).\
                     group_by(Measures.station).order_by(desc(func.count(Measures.station))).all()

    most_active = unique_counts[0][0]

    results = session.query(Measures.tobs, Measures.date).filter(Measures.station == most_active).filter(Measures.date >= year_ago).all()
    
    session.close()

    year_tobs = []
    for tob, dat in results:
        tob_dict = {}
        tob_dict[dat] = tob
        year_tobs.append(tob_dict)

    return jsonify(year_tobs)






# Accepts the start date as a parameter from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset 
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    results = session.query(func.min(Measures.tobs), func.max(Measures.tobs), func.avg(Measures.tobs))\
        .filter(Measures.date >= start).all()

    sumstats = []
    for mi, ma, av in results:
        sumdict = {}
        sumdict['min temp'] = mi
        sumdict['max temp'] = ma
        sumdict['average temp'] = av
        sumstats.append(sumdict)
    
    return jsonify(sumstats)


# Accepts the start and end dates as parameters from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the given end date
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)

    results = session.query(func.min(Measures.tobs), func.max(Measures.tobs), func.avg(Measures.tobs))\
        .filter(Measures.date >= start).filter(Measures.date <= end).all()

    sumstats = []
    for mi, ma, av in results:
        sumdict = {}
        sumdict['min temp'] = mi
        sumdict['max temp'] = ma
        sumdict['average temp'] = av
        sumstats.append(sumdict)
    
    return jsonify(sumstats)


if __name__ == '__main__':
    app.run(debug=True)

