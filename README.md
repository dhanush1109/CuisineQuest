# CuisineQuest

## Overview
This is a Flask web application that helps users find nearby restaurants and provides restaurant recommendations based on their location. Users can sign up, log in, and search for restaurants in their area.

## Installation
1. Clone this repository to your local machine:

```terminal
git clone https://github.com/dhanush1109/CuisineQuest.git
```

2. Navigate to the project directory:

```terminal
cd CuisineQuest
```

3. Create a virtual environment (recommended):

```terminal
python -m venv venv
```

4. Activate the virtual environment:
   - On Windows:
   
   ```terminal
   venv\Scripts\activate
   ```
   
   - On macOS and Linux:
   
   ```terminal
   source venv/bin/activate
   ```

5. Install the required packages:

```terminal
pip install -r requirements.txt
```

6. Extract the templates from the `templates.zip` file in the GitHub repository and place them in the `templates` directory of the project.

7. Configure MySQL database settings in `app.py`:

```python
app.config['MYSQL_HOST'] = 'YOUR_HOST_NAME'
app.config['MYSQL_USER'] = 'YOUR_DATABASE_USERNAME'
app.config['MYSQL_PASSWORD'] = 'YOUR_DATABASE_PASSWORD'
app.config['MYSQL_DB'] = 'YOUR_DATABASE_NAME'
```

8. Run the Flask application:

```terminal
python app.py
```

## Usage
- Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the application.
- Sign up for a new account or log in if you already have one.
- Search for restaurants in your area or get recommendations based on your location.

## Dependencies
- Flask: Web framework for Python.
- Flask-MySQLdb: MySQL database integration for Flask.
- scikit-learn: Machine learning library for Python.
