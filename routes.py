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
            ),
            # Center on the US
            # 40.08859435498663, -98.61733537069757
            lat=40.08859435498663,
            lng=-98.61733537069757,

            # Zoom level: 1-20, lower numbers show more area
            # zoom=3: Shows most of a continent
            # zoom=2: Shows multiple continents
            # zoom=1: Shows almost the entire world
            zoom=5,
            markers=markers,
        )
        
        return render_template('map.html', mymap=mymap)

    @app.route('/form')
    def show_form():
        return render_template('form.html')
    
    @app.route('/story')
    def show_story():
        return render_template('story.html')    
    
    @app.route('/home')
    def show_home():
        return render_template('index.html') 

    @app.route('/submit', methods=['POST'])
    def submit_form():
        if request.method == 'POST':
            # Get form data
            username = request.form.get('username', 'anonymous')
            title = request.form.get('title')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            song = request.form.get('song')
            artist = request.form.get('artist')
            
            # Insert data into database
            print(f"Inserting data for username: {username}, title: {title}, latitude: {latitude}, longitude: {longitude}, song: {song}, artist: {artist}")
            success = insert_location(username, title, latitude, longitude, song, artist)
            
            if not success:
                return "An error occurred while saving your data."
            
            return redirect(url_for('home'))
        
        return redirect(url_for('home')) 