# PyGFSTPM

> RESTful API written using Python Flask to enable users to register and then upload/download their files to a MongoDB's GridFS

### RESTful Endpoints

* ```POST /users?username=<new-username>&password=<new-password>``` *~>* register new user

* ```POST /upload/<filename>``` + (request.data contains file-contents) *~>* upload new file as authenticated user

* ```POST /configs?max_file_size=<max_size_allowed>``` *~>* admin_only endpoint to update upload limit

_Assumes MongoDB instance running on default port/settings locally without auth._

#### Default Admin Credentials:
* username: ```admin```
* password: ```admin```

_More users can be made admin through record update in MongoDB_
