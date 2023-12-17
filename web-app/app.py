
from flask import Flask, render_template, request, redirect, url_for, make_response, session, send_file
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary
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

@app.route('/AddItem', methods=['POST'])
def AddItem():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('LoginPage'))
    
    if request.method == 'POST':
        try:
            itemImage = request.files['item_image']
            category = request.form['category']
            description = request.form['description']
            condition = request.form['condition']
            price = request.form['price']

            imageData = Binary(itemImage.read())
            items = db['items']

            item_info = {
                "category": category,
                "description": description,
                "condition": condition,
                "price": price,
                "image_data": imageData,  # Save the image data as Binary in the database
                "user": session['username'],  # Include the username of the logged-in user
                "user_email": session['user_email'],  # Include the email of the logged-in user
                "user_phone": session['user_phone']  # Include the phone of the logged-in user
            }
            
            items.insert_one(item_info)
            print("item added successfuly")
            return redirect(url_for('ViewAllTrade'))
 
        except Exception as e:
            print("unable to add item")
            error = f"unable to add item: {str(e)}"
            return render_template('additem.html', error=error)

@app.route('/ViewAllTrade')
def ViewAllTrade():
    get_current_user = session.get('username', '')
    items_collection = db['items']
    all_items = items_collection.find({'user': {'$ne': get_current_user}})
    return render_template('ViewAllTrade.html', all_items=all_items)

@app.route('/ViewItemDetail/<itemId>')
def ViewItemDetail(itemId):
 
    items_collection = db['items']
    get_Individual_item = items_collection.find_one({"_id": ObjectId(itemId)})

    return render_template('ViewItemDetail.html', get_Individual_item=get_Individual_item)

@app.route('/YourTrade')
def YourTrade():
    if 'username' not in session:
        return redirect(url_for('LoginPage'))

    get_current_user = session.get('username', '')
    items_collection = db['items']
    get_my_item = items_collection.find({'user': get_current_user})
    return render_template('YourTrade.html', get_my_item=get_my_item )

@app.route('/YourItemDetail/<itemId>')
def YourItemDetail(itemId):
 
    items_collection = db['items']
    get_your_item = items_collection.find_one({"_id": ObjectId(itemId)})

    return render_template('YourItemDetail.html', get_your_item=get_your_item)


@app.route('/DeleteItem/<itemId>', methods=['POST'])
def DeleteItem(itemId):
    return

@app.route('/EditItem/<itemId>', methods=['GET'])
def EditItem(itemId):
    return


## Thank you stackOver flow: https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database
## way to access image to render for that specific entry
@app.route('/images/<itemId>')
def get_image(itemId):
    items_collection = db['items']
    get_item_image = items_collection.find_one({'_id': ObjectId(itemId)})

    if get_item_image and 'image_data' in get_item_image:
        response = make_response(get_item_image['image_data'])

        # Specify multiple content types separated by a comma
        response.headers['Content-Type'] = 'image/jpeg, image/png, image/gif'

        return response

    return 'Image not found', 404


#@app.route('/SearchForItem')
#def SearchForItem():
#    return render_template('SearchTrade.html', filtered_item_list = [])

@app.route('/SearchForItem', methods = ['GET'])
def SearchByCategory():
    items = db['items']
    filtered_item_list = []
    category_name = request.args.get('item_category', '')
    print(category_name)
    if(category_name):
        filtered_item_list = list(items.find({'category': {"$regex": category_name,  "$options": "i"}}))
        #print(filtered_item_list)
    return render_template('SearchTrade.html', filtered_item_list = filtered_item_list)
    

@app.route('/', methods=['GET', 'POST'])
def LoginPage():
    if (request.method == 'GET'):
        return render_template('login.html')
    else:
        username = request.form['fname']
        password = request.form['fpwd']

        if authenticate_user(username, password):
            # Authentication successful
            users = db['users']
            userData = users.find_one({"username": username})

            session['logged_in'] = True
            session['username'] = username

            session['user_email'] = userData.get('email', '')
            session['user_phone'] = userData.get('phone', '')
            
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

            session['logged_in'] = True
            session['username'] = name
            session['user_email'] = email
            session['user_phone'] = phone

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
