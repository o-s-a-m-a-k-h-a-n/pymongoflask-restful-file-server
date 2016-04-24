# -*- coding: utf-8 -*-
###########
# imports #
###########
import json
from flask import Flask, request, make_response, abort, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from pymongo import MongoClient
from gridfs import GridFS


################
# setup/config #
################

# set up Flask app and mongodb objects
app = Flask(__name__)
db = MongoClient().gfs_filestore
gfs = GridFS(db)
auth = HTTPBasicAuth()

# gfs_filestore.configs collection is assume to have one document 'max_file_size'
# with the maximum upload file size limit set by admin
# if document is not configured properly, default max size to 50MB
# TODO: create an admin endpoint to basic authenticate and change this value
MAX_FILE_SIZE = db.configs.find_one({"name":"max_file_size"})['max_file_size'] if db.configs.find_one({"name":"max_file_size"}) else 50000000

#############################
# HTTPBasicAuthHelperMethod #
#############################

@auth.verify_password
def verify_password(username, password):
    # as this is the most secure fileserver in the world, we will just retrieve the
    # username and password information from db, if exists, and verify user. Yay!
    record = db.users.find({"username":username})
    if record.count() > 0:
        pass
    # TODO: verify username and password
    return True



##########
# routes #
##########
@app.route('/users', methods=['GET'])
@auth.login_required
def users():
    user_list = db.users.find().count()
    return json.dumps({'results': MAX_FILE_SIZE}),200

# register new user
# NOTE: not hashing or securing password to develop contrived app for demo/text purposes
@app.route('/users', methods=['POST'])
def new_user():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if db.users.find({"username":username}).count() > 0:
        abort(400) # existing user
    new_user = db.users.insert({'username':username, 'password':password})
    if db.users.find_one(new_user) is not None:
        return jsonify({'status':'New user created successfully'}), 201
    else:
        return jsonify({'status': 'Error ocurred during user creation'})


# upload route expecting a filename in route and file contents in data
@app.route('/upload/<file_name>', methods=['POST'])
@auth.login_required
def upload(file_name):
    # TODO: link each file to user
    uploaded_file = request.data
    if len(uploaded_file) < MAX_FILE_SIZE:
        with gfs.new_file(filename=file_name) as fp:
            file_id = fp.write(uploaded_file)
            if gfs.find_one(file_id) is not None:
                return jsonify({'status': 'File saved successfully'}), 200
            else:
                return jsonify({'status': 'Error occured while saving file'}), 500
    else:
        return jsonify({'status': 'File exceeded allowed size limit'}), 500

# download route returns contents for given filename if exists in gfs
@app.route('/download/<file_name>')
@auth.login_required
def download(file_name):
    # TODO: get the username, check if the user object has such a file and return accordingly
    gfs_file = gfs.find_one({'filename': file_name})
    response = make_response(gfs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    return response

########
# main #
########
if __name__ == '__main__':
    app.run(debug=True)
