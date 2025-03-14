from flask import Flask
from flask_googlemaps import GoogleMaps
from threading import Event
import sys

from config import GOOGLE_MAPS_API, LAUNCHDARKLY_SDK_KEY, GOOGLE_MAPS_FLAG_KEY, SECRET_KEY
from routes import register_routes
from feature_flags import initialize_ldclient

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
  
    # Initialize Google Maps
    GoogleMaps(app, key=GOOGLE_MAPS_API)
    
    register_routes(app)
    
    return app

if __name__ == "__main__":
    # Check for required environment variables
    if not LAUNCHDARKLY_SDK_KEY:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        sys.exit(1)
    
    if not GOOGLE_MAPS_FLAG_KEY:
        print("*** Please set the LAUNCHDARKLY_FLAG_KEY env first")
        sys.exit(1)
    
    # Initialize LaunchDarkly client
    if not initialize_ldclient(LAUNCHDARKLY_SDK_KEY):
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        sys.exit(1)
    
    print("*** SDK successfully initialized")
    
    # Create and run the app
    app = create_app()
    try:
        app.run(host="0.0.0.0", port=8080)
        Event().wait()
    except KeyboardInterrupt:
        pass
