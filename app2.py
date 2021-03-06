from flask import Flask, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from config import connection
engine = create_engine(connection["mysql_connection"])

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Justice = Base.classes.justice_league

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/api/v1.0/all")
def all():
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Justice).all()

    # Convert list of tuples into normal list
    all_superheros = []
    for superhero in results:
    	superhero_dict = {}
    	superhero_dict["superhero"] = superhero.superhero
    	superhero_dict["real_name"] = superhero.real_name
    	all_superheros.append(superhero_dict)

    return jsonify(all_superheros)


@app.route("/api/v1.0/names")
def names():
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Justice.superhero).all()

    # Convert list of tuples into normal list
    superheros = list(np.ravel(results))

    return jsonify(superheros)


if __name__ == '__main__':
    app.run(debug=True)