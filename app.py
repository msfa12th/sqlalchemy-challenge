
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
import datetime as dt



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/><br/>"
        f"where start = start_date = mm-dd-yyyy<br/>"
        f"where end = end_date = mm-dd-yyyy<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    maxYear=session.query(func.extract('year',func.max(Measurement.date))).all() 
    maxMonth=session.query(func.extract('month',func.max(Measurement.date))).all() 
    maxDay=session.query(func.extract('day',func.max(Measurement.date))).all() 

    results=session.query(Measurement.date,Measurement.prcp)\
        .filter(Measurement.prcp != None)\
        .filter(Measurement.date >= dt.date(maxYear[0][0]-1, maxMonth[0][0], maxDay[0][0])).\
        order_by(Measurement.date).all()
    session.close()

    all_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_data.append(prcp_dict)
    
    return jsonify(all_data)


@app.route("/api/v1.0/stations")
def stations():
    
    # Return a JSON list of stations from the dataset.
    session = Session(engine)
    results=session.query(Station.name).all() 
    session.close()

    all_data = []
    for name in results:
        station_dict = {}
        station_dict["name"] = name
        all_data.append(station_dict)
    
    return jsonify(all_data)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    maxYear=session.query(func.extract('year',func.max(Measurement.date))).all() 
    maxMonth=session.query(func.extract('month',func.max(Measurement.date))).all() 
    maxDay=session.query(func.extract('day',func.max(Measurement.date))).all() 

    results=session.query(Measurement.date,Measurement.tobs)\
        .filter(Measurement.tobs != None)\
        .filter(Measurement.date >= dt.date(maxYear[0][0]-1, maxMonth[0][0], maxDay[0][0]))\
        .order_by(Measurement.date).all()
    session.close()

    all_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_data.append(tobs_dict)
        
    return jsonify(all_data)

    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    # Unpack the date and prcp from results and save into separate lists
    #dateValues = [result[0] for result in tobsResult]
    #tobsValues = [result[1] for result in tobsResult]

    # Create data frame
    #tobs = {'date': dateValues,
    #          'tobs': prcpValues}
    #tobsDF = pd.DataFrame(tobs)
    #tobsDF.set_index('date')
    #tobsDIC=tobsDF.transpose().to_dict(orient='list')
    
    # Return the JSON representation of your dictionary.


@app.route("/api/v1.0/<string:startDate>") 
def getStartDate(startDate):
    session = Session(engine)
    
    results=session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.tobs != None)\
        .filter(Measurement.date >= datetime.strptime(startDate, '%m-%d-%Y'))\
        .all()
    session.close()

    all_data = []
    for tmin,tavg,tmax in results:
        tobs_dict = {}
        tobs_dict["tmin"] = tmin
        tobs_dict["tavg"] = tavg
        tobs_dict["tmax"] = tmax
        all_data.append(tobs_dict)
        
    return jsonify(all_data)

@app.route("/api/v1.0/<string:startDate>/<string:endDate>")
def getStartEnd(startDate,endDate):
    session = Session(engine)
    
    results=session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.tobs != None)\
        .filter(Measurement.date >= datetime.strptime(startDate, '%m-%d-%Y'))\
        .filter(Measurement.date <= datetime.strptime(endDate, '%m-%d-%Y'))\
        .all()
    session.close()

    all_data = []
    for tmin,tavg,tmax in results:
        tobs_dict = {}
        tobs_dict["tmin"] = tmin
        tobs_dict["tavg"] = tavg
        tobs_dict["tmax"] = tmax
        all_data.append(tobs_dict)
        
    return jsonify(all_data)


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

