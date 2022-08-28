import os
from flask import Flask, session, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='pitanguinha',
        MYSQL_HOST='localhost',
        MYSQL_USER='root',
        MYSQL_PASSWORD='Gr&mio9966',
        MYSQL_DB='data'
    )
    mysql = MySQL(app)

    app.static_folder = 'static'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/home')
    def home():
        return 'LOGOUUU'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Output message if something goes wrong...
        msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:        
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_name = %s AND password = %s', (username, password))
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id_user']
                session['username'] = account['user_name']
                # Redirect to home page
                return redirect('/home')
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
        # Show the login form with message (if any)
        return render_template('login.html', msg=msg)

    @app.route('/signup')
    def signup():
        return 'LOGA AI'

    @app.route('/logout')
    def logout():
        return 'Logout'

    return app