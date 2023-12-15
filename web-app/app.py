
from flask import Flask, render_template, request, redirect, url_for, make_response, session
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt



app = Flask('Trader')
app.secret_key = 'pass'

client = MongoClient("mongodb://localhost:27017/")
db = client["trade_database"]

@app.route('/Trade')
def RootPage():
    return render_template('rootpage.html')

@app.route('/AddItem')
def AddItemPage():
    return render_template('additem.html')

@app.route('/ViewAllTrade')
def ViewAllTrade():
    return render_template('ViewAllTrade.html')

@app.route('/YourTrade')
def ViewYourTrade():
    return render_template('YourTrade.html')

@app.route('/SearchForItem')
def SearchForItem():
    return render_template('SearchTrade.html')

@app.route('/', methods=['GET', 'POST'])
def LoginPage():
    if (request.method == 'GET'):
        return render_template('login.html')
    else:
        username = request.form['fname']
        password = request.form['fpwd']

        if authenticate_user(username, password):
            # Authentication successful
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('RootPage'))
        else:
            error = "Login Failed: Invalid username or password."
            return render_template('login.html', error=error)
    
@app.route('/register', methods=['GET', 'POST'])
def RegisterPage():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['fname']
        pwd = request.form['fpwd']
        email = request.form['femail']
        phone = request.form['fnumber']
        
        if register_user(name, pwd, email, phone):
            # Registration successful, print a message and redirect
            print(f"User '{name}' registered successfully.")
            return redirect(url_for('LoginPage'))
        else:
            # Registration failed, print an error message
            print(f"Failed to register user '{name}'.")
            error = 'Username already exist please create a new one'
            return render_template('register.html', error=error)
        
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session data
    return redirect(url_for('LoginPage'))

def register_user(username, password, email, phone):
    try:
        # check if user exist 
        users = db['users']
        ExistingUser = users.find_one({
            "$or": [
                {"username": username},
                {"email": email},
                {"phone": phone}
            ]
        })

        if (ExistingUser):
            return False
        print(f"hi")
        # Insert user data into the 'users' collection
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))  # Set work factor to 10
        user_data = {"username": username, "password": hashed_password, "email": email, "phone": phone}
        users.insert_one(user_data)
        print(f"User registered: {user_data}")
        return True
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return False

def authenticate_user(username, password):
    users = db['users']
    user = users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False

@app.route('/Profile', methods=['GET', 'POST'])
def UserProfile():
    if 'username' not in session:
        return redirect(url_for('LoginPage'))

    users = db['users']
    current_user = session['username']
    user_data = users.find_one({"username": current_user})

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_phone = request.form['phone']

        if new_username != current_user:
            session['username'] = new_username

        users.update_one({"username": current_user}, {"$set": {"username": new_username, "email": new_email, "phone": new_phone}})
        return redirect(url_for('UserProfile'))

    return render_template('profile.html', user=user_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
