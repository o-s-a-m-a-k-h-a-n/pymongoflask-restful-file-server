# -*- coding: utf-8 -*-

import json
from flask import Flask, request, make_response
from pymongo import MongoClient
from gridfs import GridFS

app = Flask(__name__)
db = MongoClient().gfs_filestore
gfs = GridFS(db)
MAX_FILE_SIZE = db.configs.find_one({"name":"max_file_size"})['max_file_size']

@app.route('/users', methods=['GET'])
def users():
    user_list = db.users.find().count()
    return json.dumps({'results': MAX_FILE_SIZE}),200

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

@app.route('/download/<file_name>')
def download(file_name):
    gfs_file = gfs.find_one({'filename': file_name})
    response = make_response(gfs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    return response

if __name__ == '__main__':
    app.run(debug=True)
