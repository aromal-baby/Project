from crbnftprnt import app, db


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully")
        except Exception as e:
            print(f"Error creating database: {e}")
    
    app.run(debug=True)