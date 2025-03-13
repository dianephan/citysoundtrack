import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, session, url_for, send_file
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
from flask_googlemaps import GoogleMaps, Map
import sqlite3
from sqlite3 import Error

load_dotenv()
# didn't even need the api to just show the map 
GOOGLE_MAPS_API = os.environ.get('GOOGLE_MAPS_API')

app = Flask(__name__)
GoogleMaps(app, key=GOOGLE_MAPS_API)
UPLOAD_FOLDER = "static"
BUCKET = "lats-image-data"

app.secret_key = 'dsfdgfdg;sdyyuyy'
markers = [] 


# #############################################################
#
# map route
# 
# if flag is on, render map of movies only
# if flag is off, render map of crowdsourced data
# OR
# if flag is on, render map with california coordinates
# if flag is off, render map with new york coordinates
# 
# #############################################################

@app.route('/map')
def mapview(): 
  try:
      conn = sqlite3.connect('app.db')
      print("Successful connection!")
      cur = conn.cursor()
      retrieve_url_query = """SELECT user, title, latitude, longitude, song, artist FROM locations;"""
      cur.execute(retrieve_url_query)      
      music_data = cur.fetchall()
      for entry in music_data: 
        print("[DATA] : parsed entry = ", entry)          
        markers.append({
          'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
          'lat': entry[2], 
          'lng': entry[3],
          'infobox': '<div id="bodyContent">' +
                     '<p><b>Movie:</b> ' + entry[1] + '</p>' +
                     '<p><b>Song:</b> ' + entry[4] + '</p>' +
                     '<p><b>Artist:</b> ' + entry[5] + '</p>' +
            '' + '</div>'           
        })

  except sqlite3.Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      print('Uh-oh')
  
  # if flag is off, render map with movie data
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
    lat=37.805355,
    lng=-122.322618,
    markers=markers,
  )

  # if flag is on, render map with crowdsourced data

    
  return render_template('map.html', mymap=mymap)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/form')
def show_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        try:
            # Get form data
            user = request.form.get('user')
            title = request.form.get('title')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            song = request.form.get('song')
            artist = request.form.get('artist')
            
            # Connect to database
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            print("Data successfully inserted into database")
            # Insert data into database
            insert_query = """
                INSERT INTO locations (user, title, latitude, longitude, song, artist)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cur.execute(insert_query, (user, title, latitude, longitude, song, artist))
            conn.commit()
            
            print("Data successfully inserted into database")
            return redirect(url_for('home'))
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return "An error occurred while saving your data."
        finally:
            if conn:
                conn.close()
    
    return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
