import os
from flask import Flask
from models.database import init_db

# Create data directory
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created data directory at {data_dir}")

app = Flask(__name__)

init_db(app)

print("Database setup complete.")