import random
import datetime
import flask
from flask import jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///sacaar.db'
db = SQLAlchemy(app)


participants = db.Table('participants',
                       db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
                       db.Column('batttle_id', db.Integer, db.ForeignKey('battle.id')))


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    victory = db.Column(db.Integer, default=0)
    defeat = db.Column(db.Integer, default=0)
    death_date = db.Column(db.DateTime)
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    battles = db.relationship('Battle', secondary=participants, backref=db.backref('characters', lazy='dynamic'))

    def __repr__(self):
        return f'{self.name} {self.race} {self.victory} {self.defeat} {self.death_date}'

class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    characters = db.relationship('Character', backref='race')

    def __repl__(self):
        return f' {self.race}'

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    def __repr__(self):
        return f'Battle {self.id}'



@app.route('/')
def get_index():
    return 'Welcome to the Sacaar Battles!'


@app.route('/characters')
def get_characters():
    results = Character.query.filter_by(death_date=None).order_by((Character.victory - Character.defeat).desc()).join(Race).all()
    res = [{"name": result.name, "race": result.race.name, "victory": result.victory, "defeat": result.defeat} for result in results]
    return jsonify({"characters": res})


@app.route('/killed')
def get_killed_characters():
    results = Character.query.filter(Character.death_date != None).order_by(Character.victory.desc()).join(Race).all()
    res = [{"name": result.name, "race": result.race.name, "victory": result.victory, "death_date": result.death_date} for
           result in results]
    return jsonify({"killed": res})


@app.route('/battle')
def get_battle():
    races = Race.query.all()
    while races:
        fighters = Character.query.filter_by(death_date=None).all()
        first_fighter = random.choice(fighters)
        last_battle = first_fighter.battles[-1:]
        if last_battle:
            last_participants_ids = {char.id for char in last_battle.characters}
        else:
            last_participants_ids = {first_fighter.id}
        remaining_fighters = [char for char in fighters if (char.race_id == first_fighter.race_id) \
                                                        and (char.id not in last_participants_ids)]
        if remaining_fighters:
            second_fighter = random.choice(remaining_fighters)
            battle = Battle()
            battle.characters.append(first_fighter)
            battle.characters.append(second_fighter)
            db.session.add(battle)
            db.session.commit()
            return make_response(jsonify({"battle": {
                "first fighter": {"name": first_fighter.name, "race": first_fighter.race.name},
                "second fighter": {"name": second_fighter.name, "race": second_fighter.race.name}}}))
        races.remove(first_fighter.race)
    return jsonify("No fighters remaining")



@app.route('/kill/<int:id>', methods=['POST'])
def kill(id):
    character = Character.query.filter_by(id=id).first()
    if character:
        if character.death_date:
            return jsonify(f"Character ID {id} has already been killed. Time {character.death_date}")
        character.death_date = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify({"killed": {"name": character.name, "death_date": character.death_date}})
    return make_response(jsonify(f"Character ID {id} doesn't exist"), 404)



if __name__ == '__main__':
    app.run(debug=True)