#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from ntpath import join
from os import abort
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
        return f'< id: {self.id} , name:{self.name},genres:{self.genres}, city:{self.city}, state:{self.state}, seeking_talent:{self.seeking_talent} >'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(250))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_description = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean())
    website_link = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'< id: {self.id} , name:{self.name},genres:{self.genres}, city:{self.city}, state:{self.state}, seeking_talent:{self.seeking_talent} >'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    start_time = db.Column(db.DateTime())

    def __repr__(self):
        return f'< id: {self.id} , artist_id:{self.artist_id},venue_id:{self.venue_id}, start_time:{self.start_time} >'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #   num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = {}
    error = False
    try:
        data = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()
    except:
        error = True
    finally:
        if error:
            abort(400)
        else:
            return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = {}
    error = False
    try:
        data = Venue.query.filter_by(id=venue_id).first()
    except:
        error = True
    finally:
        if error:
            abort(400)
        else:
            return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    data = {}
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.get('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')

        seeking_description = request.form.get('seeking_description')
        if request.form.get('seeking_talent') == 'y':
            seeking_talent = True

        else:
            seeking_talent = False
            data = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres,
                         facebook_link=facebook_link, website_link=website_link, seeking_description=seeking_description, seeking_talent=seeking_talent)
            db.session.add(data)
            db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        if error:
            abort(400)
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
            return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # licking that button delete it from the db then redirect the user to the homepage
    data = {}
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        if error:
            abort(400)
        else:
            return redirect(url_for('venue'))


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = {}
    error = False
    try:
        data = Artist.query.all()
    except:
        error = True
    finally:
        if error:
            abort(400)
        else:
            return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data = {}
    error = False
    try:
        data = Artist.query.filter_by(id=artist_id).first()
    except:
        error = True
    finally:
        if error:
            abort(400)
        else:
            return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    data = Artist.query.filter_by(id=artist_id).first()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    data = Venue.query.filter_by(id=venue_id).first()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    data = {}
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.get('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')

        seeking_description = request.form.get('seeking_description')
        if request.form.get('seeking_talent') == 'y':
            seeking_talent = True

        else:
            seeking_talent = False

        # TODO: modify data to be the data object returned from db insertion
        artistData = Artist(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, genres=genres,
                            facebook_link=facebook_link, website_link=website_link, seeking_description=seeking_description, seeking_talent=seeking_talent)
        db.session.add(artistData)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        if error:
            abort(400)
        else:
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
            return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = {}
    error = False

    try:
        data = db.session.query(Show.artist_id, Show.venue_id, Show.start_time, Artist.name, Artist.image_link, Venue.name).join(
            Artist, Show.artist_id == Artist.id).join(Venue, Show.venue_id == Venue.id).all()
    except:
        error = True
    finally:
        if error:
            abort(400)
        else:
            return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    data = {}
    error = True
    try:
        venue = request.form.get('venue_id')
        artist = request.form.get('artist_id')
        start = request.form.get('start_time')

        # TODO: insert form data as a new Show record in the db, instead
        show = Show(venue_id=venue, artist_id=artist, start_time=start)
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        if error:
            abort(400)
        else:
            # on successful db insert, flash success
            flash('Show was successfully listed!')
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
