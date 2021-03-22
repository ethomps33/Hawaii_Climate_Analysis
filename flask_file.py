# 1. import Flask
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route

@app.route("/")
def Home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    
    )  


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = dt.datetime(2017, 8, 23) - dt.timedelta(days = 365)

    active_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_date).\
        order_by(desc(Measurement.date)).all()

    session.close()

    tobs_list = list(np.ravel(active_temp))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)

    temps = session.execute("SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM Measurement WHERE date > '2013-04-01'").fetchall()

    temps_start = list(np.ravel(temps))

    return jsonify(temps_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    session = Session(engine)

    temps = session.execute("SELECT MIN(tobs), MAX(tobs), AVG(tobs) FROM Measurement WHERE date > '2013-04-01' AND date < 2015-01-01").fetchall()

    temps_end = list(np.ravel(temps))

    return jsonify(temps_end)
if __name__ == "__main__":
    app.run(debug=True)

