# Import  factory function from  package
from chess_engine import create_app

# Call the function to create the app instance
app = create_app()

if __name__ == "__main__":
    # . Run the application
    app.run(debug=True)
