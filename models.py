import psycopg2
from psycopg2 import Error
from config import DATABASE_URI

def get_db_connection():
    """Create a database connection to the PostgreSQL database"""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URI)
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
            
            retrieve_url_query = """SELECT username, title, latitude, longitude, song, artist FROM locations WHERE username != 'diane';"""
            cur.execute(retrieve_url_query)      
            music_data = cur.fetchall()
            
            for entry in music_data:
                # print("[DATA] : parsed crowdsourced entry = ", entry)          
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
            retrieve_url_query = """SELECT username, title, latitude, longitude, song, artist FROM locations WHERE username = 'diane';"""
            cur.execute(retrieve_url_query)      
            music_data = cur.fetchall()
            
            for entry in music_data:
                # print("[DATA] : parsed movie entry = ", entry)          
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
    """Fetch all locations from the PostgreSQL database"""
    conn = get_db_connection()
    markers = []
    
    if conn:
        try:
            cur = conn.cursor()
            retrieve_url_query = """SELECT username, title, latitude, longitude, song, artist FROM locations;"""
            cur.execute(retrieve_url_query)      
            music_data = cur.fetchall()
            
            for entry in music_data: 
                # print("[DATA] : parsed entry = ", entry)          
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
                
            # Close the cursor (but keep connection open for other functions)
            cur.close()
            
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    return markers

def insert_location(username, title, latitude, longitude, song, artist):
    """Insert a new location into the database"""
    conn = get_db_connection()
    
    # Set default username if none provided
    if username is None or username == "":
        username = "anonymous" 
    
    if conn:
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO locations (username, title, latitude, longitude, song, artist)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            cur.execute(insert_query, (username, title, latitude, longitude, song, artist))

            if username == 'diane':
                insert_movie_query = """
                    INSERT INTO movies (title)
                    VALUES (%s);
                """
                cur.execute(insert_movie_query, (title,))

            else:
                insert_user_query = """
                    INSERT INTO crowdsourced_data (username)
                    VALUES (%s);
                """
                cur.execute(insert_user_query, (username,))
            conn.commit()
            
            print("Data successfully inserted into database")
            return True
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    
    return False 