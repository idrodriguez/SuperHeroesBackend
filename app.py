# import libraries
from bson.json_util import dumps
from bson.objectid import ObjectId
from envparse import env
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

# Flask app definition
app = Flask(__name__)
app.config["MONGO_URI"] = env('MONGODB_URI')
mongo = PyMongo(app)

# Routing definition
@app.route('/')
def superheroes():
    superheroes = mongo.db.SuperHero.find()
    resp = dumps(superheroes)
    return resp

@app.route('/add', methods=['POST'])
def add_superhero():
    _json = request.json
    _name = _json['name']
    _photo = _json['photo']
    _description = _json['description']
    _moreinfolink = _json['moreinfolink']
    _powers = _json['powers']

    if _name and request.method == 'POST':
        id = mongo.db.SuperHero.insert({'name': _name, 'photo' : _photo, 'description' : _description, 'moreinfolink' :  _moreinfolink, 'powers' : _powers})
        resp = jsonify('SuperHero Added')
        resp.status_code = 200
        return resp
    else:
        return not_found

@app.route('/<id>')
def superhero(id):
    superhero = mongo.db.SuperHero.find_one({'_id': ObjectId(id)})
    resp = dumps(superhero)
    return resp

@app.route('/update', methods=['PUT'])
def update_superhero():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _photo = _json['photo']
    _description = _json['description']
    _moreinfolink = _json['moreinfolink']
    _powers = _json['powers']

    if _name and request.method == 'POST':
        mongo.db.SuperHero.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'photo': _photo, 'description': _description, 'moreinfolink' : _moreinfolink, 'powers' : _powers}})
        resp = jsonify('SuperHero updated')
        resp.status_code = 200
        return resp
    else:
        return not_found

@app.route('/delete/<id>', methods=['DELETE'])
def delete_superhero(id):
    mongo.db.SuperHero.delete_one({'_id' : ObjectId(id)})
    resp = jsonify('SuperHero deleted')
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not Found: ' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__=="__name__":
    app.run(debug=True)