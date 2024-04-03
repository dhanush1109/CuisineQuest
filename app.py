from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
from sklearn.neighbors import BallTree
import numpy as np

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'YOUR_HOST_NAME'
app.config['MYSQL_USER'] = 'YOUR_DATABASE_USERNAME'
app.config['MYSQL_PASSWORD'] = 'YOUR_DATABASE_PASSWORD'
app.config['MYSQL_DB'] = 'YOUR_DATABSE_NAME'

mysql = MySQL(app)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Restaurant:
    def __init__(self, id, name, latitude, longitude, cuisine_type, rating):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.cuisine_type = cuisine_type
        self.rating = rating

# Connect to MySQL and retrieve restaurant data
def get_restaurants():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM restaurant")
    restaurants_data = cursor.fetchall()
    cursor.close()

    restaurants = []
    for data in restaurants_data:
        restaurant = Restaurant(*data)
        restaurants.append(restaurant)

    return restaurants

# Construct a BallTree for nearest neighbor search
def construct_ball_tree():
    restaurants = get_restaurants()
    restaurant_coords = np.array([(r.latitude, r.longitude) for r in restaurants])
    tree = BallTree(restaurant_coords, leaf_size=15, metric='haversine')
    return tree

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user = User(*user_data)
            # You may want to implement a session or another authentication mechanism here
            return redirect('/search_results')
        else:
            error_message = "Invalid username or password. Please try again."

        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()

        return redirect('/')

    return render_template('signup.html')

@app.route('/search_results')
def search_results():
    restaurants = get_restaurants()
    return render_template('search_results.html', restaurants=restaurants)

@app.route('/recommend', methods=['GET'])
def recommend():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    radius = float(request.args.get('radius'))

    # Construct a BallTree for nearest neighbor search
    tree = construct_ball_tree()

    # Perform KNN search to find nearest restaurants within the specified radius
    indices = tree.query_radius(np.array([[latitude, longitude]]), r=radius / 111.0)  # Convert radius from km to degrees (approximate)
    
    # Retrieve recommended restaurants from the indices obtained
    recommended_restaurants = [get_restaurants()[idx] for idx in indices[0]]

    return render_template('result.html', restaurants=recommended_restaurants)

if __name__ == '__main__':
    app.run(debug=True)
