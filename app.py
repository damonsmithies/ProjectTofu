# app.py
# Import libraries for Flask, Supabase, and API calls
from flask import Flask
import requests
from supabase import create_client, Client
import os
import threading
import time

app = Flask(__name__)

# Initialize Supabase client
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Function to pull and store API data
def pull_api_data():
    while True:
        try:
            # Pull data from API
            response = requests.get('https://jsonplaceholder.typicode.com/posts')
            data = response.json()

            # Insert into Supabase
            for item in data[:5]:
                response = supabase.table('posts').insert({
                    'id': item['id'],
                    'title': item['title'],
                    'body': item['body']
                }).execute()
                if hasattr(response, 'error') and response.error:
                    print(f"Error inserting post {item['id']}: {response.error}")
                else:
                    print(f"Inserted post {item['id']}")
        except Exception as e:
            print(f"Error in API pull: {e}")
        time.sleep(3600)  # Run every hour (adjust as needed)

# Start API pull in a background thread
threading.Thread(target=pull_api_data, daemon=True).start()

# Health endpoint to prevent sleep
@app.route('/healthz')
def healthz():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)