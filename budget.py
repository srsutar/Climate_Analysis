import pandas as pd
import datetime as dt 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Create engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect 

base = automap_base()

base.prepare(engine, reflect=True)

measurment = base.classes.measurment
station= base.classes.station

#Create session(link python to db)

session = Session(engine)

#setting up flask

cli_app = Flask(__name__)

#define the routes

@cli_app.route("/")
def Welcome_page():
    return (
       f"Welcome to Tropical Hawaiian Climate Analysis!!!<br/>" 
       f"Pathways to Discover<br/>"
       f"/precipitation_data"
       f"/station_data"
       f"/temperature_observed"
    )

@cli_app.route("/precipitation_data")
def precipitation_data():
 #date for previous year
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    preci_scores = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date>=prev_year).all()
    #create a dict. with date as key and pre as value
    prec = {date: prcp for date, prcp in preci_score}
    return jsonify(prec)

@cli_app.route("/station_data")
def station_data():
    sta = session.query(func.count(station.station)).all()
    sta_new = list(np.ravel(sta))
    return jsonify(sta_new)

@cli_app.route("/temperature_observed")
def temperature_observed():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    new_save = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()
    temp = list(np.ravel(new_save))
    return jsonify(temp)

if __name__=="__main__":
    cli_app.run()