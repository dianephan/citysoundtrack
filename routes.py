from flask import render_template, redirect, url_for, request
from flask_googlemaps import Map
from models import fetch_crowdsourced_locations, fetch_movie_locations, fetch_locations, insert_location
from feature_flags import get_flag_value
from config import GOOGLE_MAPS_FLAG_KEY

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/map')
    def mapview():
        # Check the value of the feature flag
        maps_flag_value = get_flag_value(GOOGLE_MAPS_FLAG_KEY)
        # Fetch appropriate markers based on flag value
        if maps_flag_value == True:
            print("Google Maps flag is on - showing movie locations")
            markers = fetch_movie_locations()
        if maps_flag_value == False:
            print("Google Maps flag is off - showing crowdsourced locations") 
            markers = fetch_crowdsourced_locations()        
        # Create map
        mymap = Map(
            identifier="sndmap",
            style=(
                "height:100%;"
                "width:100%;"
                "top:0;"
                "position:absolute;"
                "z-index:200;"
                "zoom: -9999999;"
            ),
            # these coordinates re-center the map
            lat=40.7527,
            lng=-73.9772,
            markers=markers,
        )
        
        return render_template('map.html', mymap=mymap)

    @app.route('/form')
    def show_form():
        return render_template('form.html')

    @app.route('/submit', methods=['POST'])
    def submit_form():
        if request.method == 'POST':
            # Get form data
            user = request.form.get('user')
            title = request.form.get('title')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            song = request.form.get('song')
            artist = request.form.get('artist')
            
            # Insert data into database
            success = insert_location(user, title, latitude, longitude, song, artist)
            
            if not success:
                return "An error occurred while saving your data."
            
            return redirect(url_for('mapview'))
        
        return redirect(url_for('home')) 