import sqlite3
from sqlite3 import Error

def get_db_connection():
    """Create a database connection"""
    conn = None
    try:
        conn = sqlite3.connect('app.db')
        return conn
    except Error as e:
        print(e)
    return conn

def fetch_crowdsourced_locations():
    """Fetch only user-submitted locations from the database"""
    conn = get_db_connection()
    markers = []
    
    if conn:
        try:
            cur = conn.cursor()
            retrieve_url_query = """SELECT user, title, latitude, longitude, song, artist FROM locations WHERE user != 'diane';"""
            cur.execute(retrieve_url_query)      
            music_data = cur.fetchall()
            
            for entry in music_data:
                print("[DATA] : parsed crowdsourced entry = ", entry)          
                markers.append({
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                    'lat': entry[2], 
                    'lng': entry[3],
                    'infobox': '<div id="bodyContent">' +
                        '<p><b>Title:</b> ' + entry[1] + '</p>' +
                        '<p><b>Song:</b> ' + entry[4] + '</p>' +
                        '<p><b>Artist:</b> ' + entry[5] + '</p>' +
                    '' + '</div>'           
                })
        except Error as e:
            print(e)
        finally:
            conn.close()
    return markers

def fetch_movie_locations():
    """Fetch only movie locations from the database (where user is diane)"""
    conn = get_db_connection()
    markers = []
    
    if conn:
        try:
            cur = conn.cursor()
            retrieve_url_query = """SELECT user, title, latitude, longitude, song, artist FROM locations WHERE user = 'diane';"""
            cur.execute(retrieve_url_query)      
            music_data = cur.fetchall()
            
            for entry in music_data:
                print("[DATA] : parsed movie entry = ", entry)          
                markers.append({
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                    'lat': entry[2], 
                    'lng': entry[3],
                    'infobox': '<div id="bodyContent">' +
                        '<p><b>Movie:</b> ' + entry[1] + '</p>' +
                        '<p><b>Song:</b> ' + entry[4] + '</p>' +
                        '<p><b>Artist:</b> ' + entry[5] + '</p>' +
                    '' + '</div>'           
                })
        except Error as e:
            print(e)
        finally:
            conn.close()
    return markers

def fetch_locations():
    """Fetch all locations from the database"""
    conn = get_db_connection()
    markers = []
    
    if conn:
        try:
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
        except Error as e:
            print(e)
        finally:
            conn.close()
    return markers

def insert_location(user, title, latitude, longitude, song, artist):
    """Insert a new location into the database"""
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO locations (user, title, latitude, longitude, song, artist)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cur.execute(insert_query, (user, title, latitude, longitude, song, artist))
            conn.commit()
            print("Data successfully inserted into database")
            return True
        except Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    return False 