#!/usr/bin/python3
from models.app import create_app
from models.user import db

app = create_app()

# Use the app context
with app.app_context():
    # Print the URI to check if it's correct
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Create the database tables
    db.create_all()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
