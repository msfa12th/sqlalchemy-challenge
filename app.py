
from flask import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
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
    results=session.query(Measurement.date,Measurement.tobs)\
        .filter(Measurement.tobs != None)\
        .filter(Measurement.date >= dt.date(maxYear[0][0]-1, maxMonth[0][0], maxDay[0][0]))\
        .filter(Measurement.station == 'USC00519281')\
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


@app.route("/api/v1.0/<start>")
def start():
    email = "peleke@example.com"

    return f"What is the start date? {email}."

@app.route("/api/v1.0/<start>/<end>")
def contact():
    email = "peleke@example.com"

    return f"Tell me the start and end date {email}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

    
    import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

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
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
