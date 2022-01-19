"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 

debug=DebugToolbarExtension(app)

from models import db, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True       

connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""
    return {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}

@app.route("/")
def show_cupcake_form():
    return render_template("cupcake-form.html")

@app.route("/api/cupcakes", methods=["GET"])
def get_cupcakes():
    """Get data about all cupcakes in JSON"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<cupcake_id>")
def get_cupcake(cupcake_id):
    """Get data about a single cupcake in JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data and return it in JSON"""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/ status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)



@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    Cupcake.query.filter(Cupcake.id == cupcake_id).delete()

    db.session.commit()

    return jsonify({"message": "Deleted"})

    






