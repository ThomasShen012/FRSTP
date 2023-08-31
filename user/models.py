from flask import Flask, jsonify, request, render_template,session,redirect,Response
import pymongo
import json
from bson import json_util
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from  flask_login import  login_user, login_required, logout_user, current_user


myclient = pymongo.MongoClient("mongodb+srv://team17:TqZI3KaT56q6xwYZ@team17.ufycbtt.mongodb.net/")
mydb = myclient.test

class User:

    def start_session(self, user):
        del user['password']
        user_json = json_util.dumps(user)
        session['logged_in'] = True
        session['user'] = user_json
        return user_json

    def signup(self):
        user = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "gender": request.form.get('gender'),
            "birthday": request.form.get('birthday')
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        user_json = json_util.dumps(user)

        #checking for existing email
        if mydb.users.find_one({ "email": user['email']}):
           return jsonify({ "error": "email address already exist"}), 400
        
        if mydb.users.insert_one(user):
    
            return self.start_session(user)
        
        return jsonify({"error": "sign up error"}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = mydb.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid" }), 401
    
    def update_user(self, _id):
        user_id = ObjectId(_id)  # Convert the string id to ObjectId
        user_updates = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "gender": request.form.get('gender'),
            "birthday": request.form.get('birthday')
        }

        # Only update fields that have been provided in the form
        update_data = {key: value for key, value in user_updates.items() if value}

        # Update the user document in the database
        result = mydb.users.update_one({"_id": user_id}, {"$set": update_data})

        if result.modified_count > 0:
            # Fetch the updated user document
            updated_user = mydb.users.find_one({"_id": user_id})
            return json_util.dumps(updated_user)

        return jsonify({"error": "update error"}), 400

