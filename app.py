# -*- coding: utf-8 -*-
###########
# imports #
###########
import json
from flask import Flask, request, make_response
from pymongo import MongoClient
from gridfs import GridFS

################
# setup/config #
################

# set up Flask app and mongodb objects
app = Flask(__name__)
db = MongoClient().gfs_filestore
gfs = GridFS(db)

# gfs_filestore.configs collection is assume to have one document 'max_file_size'
# with the maximum upload file size limit set by admin
# if document is not configured properly, default max size to 50MB
# TODO: create an admin endpoint to basic authenticate and change this value
MAX_FILE_SIZE = db.configs.find_one({"name":"max_file_size"})['max_file_size'] if db.configs.find_one({"name":"max_file_size"}) else 50000000

##########
# routes #
##########
@app.route('/users', methods=['GET'])
def users():
    user_list = db.users.find().count()
    return json.dumps({'results': MAX_FILE_SIZE}),200

# upload route expecting a filename in route and file contents in data
@app.route('/upload/<file_name>', methods=['POST'])
def upload(file_name):
    uploaded_file = request.data
    if len(uploaded_file) < MAX_FILE_SIZE:
        with gfs.new_file(filename=file_name) as fp:
            file_id = fp.write(uploaded_file)
            if gfs.find_one(file_id) is not None:
                return json.dumps({'status': 'File saved successfully'}), 200
            else:
                return json.dumps({'status': 'Error occured while saving file'}), 500
    else:
        return json.dumps({'status': 'File exceeded allowed size limit'}), 500

# download route returns contents for given filename if exists in gfs
@app.route('/download/<file_name>')
def download(file_name):
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
