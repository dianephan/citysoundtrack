import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
GOOGLE_MAPS_API = os.environ.get('GOOGLE_MAPS_API')
LAUNCHDARKLY_SDK_KEY = os.environ.get('LAUNCHDARKLY_SDK_KEY')
GOOGLE_MAPS_FLAG_KEY = "googlemaps"
SECRET_KEY = 'dsfdgfdg;sdyyuyy' 
DATABASE_URI = os.environ.get('DATABASE_URI') 
