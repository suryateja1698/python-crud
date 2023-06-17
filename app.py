from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://manager@localhost/realmadrid'
db = SQLAlchemy(app)

class Player(db.Model):
    # If we want to create table in different name 'players', by default it
    # used class name
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)

# To create table
with app.app_context():
    db.create_all()

@app.route('/players', methods=['POST'])
def create_player():
    try:
        data = request.json
        player = Player(name=data['name'], age=data['age'], country=data['country'], position=data['position'])
        db.session.add(player)
        db.session.commit()
        return jsonify({'message': 'Player created successfully.'}), 201
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig') or e)
        return jsonify({'error': error}), 500

@app.route('/players', methods=['GET'])
def get_all_players():
    players = Player.query.all()
    result = []
    for player in players:
        result.append({
            'id': player.id,
            'name': player.name,
            'age': player.age,
            'country': player.country,
            'position': player.position
        })
    return jsonify(result), 200

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get(player_id)
    if player:
        return jsonify({
            'id': player.id,
            'name': player.name,
            'age': player.age,
            'country': player.country,
            'position': player.position
        }), 200
    return jsonify({'error': 'Player not found.'}), 404

@app.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    try:
        player = Player.query.get(player_id)
        if player:
            data = request.json
            player.name = data['name']
            player.age = data['age']
            player.country = data['country']
            player.position = data['position']
            db.session.commit()
            return jsonify({'message': 'Player updated successfully.'}), 200
        return jsonify({'error': 'Player not found.'}), 404
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig') or e)
        return jsonify({'error': error}), 500

@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get(player_id)
    if player:
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully.'}), 200
    return jsonify({'error': 'Player not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
