# CRUD with Flask and Vue

## Flask Setup
Setup for your Flask app
```bash
mkdir flask-vue-crud
cd flask-vue-crud
virtualenv -p python3.7 venv
source venv/bin/activate
pip install flask flask_cors redis
pip freeze > requirements.txt
touch app.py .gitignore README.md
```

Write in your `.gitignore` file
```
venv/
.Idea/
*.pyc
```

Write in your `app.py` file
```python
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "localhost:5000"}})
app.config['SECRET_KEY'] = 'all right then keep your secrets'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
  
  
@app.route('/')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def index():  
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```

Run your application and go to http://0.0.0.0:5000/
```bash
python app.py

# Terminal output after running your app.py 
* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 760-681-493
```

Make a `templates` directory parallel to your `app.py` file for your html files and then make an `index.html` file inside it
```
mkdir templates
touch templates/index.html
```

Write in your index.html
```
<!DOCTYPE html>
<html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport"  content="width=device-width,initial-scale=1.0">
      <title>Index</title>
  </head>
  <body>
      <h1>Hello</h1>
  </body>
</html>
```

## Redis Setup

This guide assumes that your Redis is already set up but if not check out this tutorial by Digitial Ocean: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

## Flask CRUD functions

Make a file called `crud_funcs.py`. This is where we're going to put our database query functions

```python
from redis import Redis
import json

# Redis server
r_server = Redis(host='localhost',port='6379', db='0')

if __name__ == "__main__":
    pass
```

**These upcoming functions will be added in your `crud_funcs.py` file**

Create/Update function
> Set or update item in Redis. Argument passed should be a dictionary like so `{"key": "your-key", "details": "your-details"}`
```python
...
def create_item(item_dict):

    """
    Set/Update item in Redis

    Args: 
        item_dict(dictionary): item 
        to be put/updated in Redis
    """
    
    try:
        json_dict = json.dumps(item_dict)
        item_key = item_dict["key"]
        r_server.set(item_key, json_dict)
        result = {"status": 1, "message": "Item Created", "item": item_dict}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
...
```

Read function
> Query redis using the redis_key argument supplied. Argument passed is a string like so `"0001"`
```python
...
def get_items(redis_key):

    """
    Get item(s) in Redis

    Args:
        redis_key(str): string for 
        scan match
    """

    cursor_ = 0
    match_ = "{}*".format(redis_key)

    try:
        
        cursor, keys_ = r_server.scan(cursor=cursor_, match=match_)

        r_response = r_server.mget(keys_)
        json_val_list = []
        
        # Jsonify object(s)
        for val_ in r_response:
            json_val = json.loads(val_)
            json_val_list.append(json_val)

        result = json_val_list

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
...
```

Delete function
> Delete item in Redis. Argument passed should be a dictionary like so `{"key": "your-key"}`
```python
...
def delete_item(item_):

    """ 
    Delete item in Redis

    Args: 
        item_(dictionary): item 
        to be deleted in Redis
    """

    try:
        item_key = item_["key"]
        r_server.delete(item_key)
        result = {"status": 1, "message": "Item Deleted", "item_key": item_key}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result
...
```
Back in your `app.py` file, import your crud functions and add a route for your api
```python
...
from crud_funcs import create_item, delete_item, get_items
...
@app.route('/dashboard_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def dashboard_api():

    result = None

    if request.method == 'GET':

        # Get/Update
        redis_key = request.args.get("key")
        response = get_items(redis_key)
        result = response

    elif request.method == 'POST' or request.method == 'PUT':

        # Create/Update
        item_ = request.data
        json_item = json.loads(item_)
        response = create_item(json_item)
        result = response

    elif request.method == 'DELETE':

        # Delete
        item_ = request.data
        json_item = json.loads(item_)
        response = delete_item(json_item)
        result = response

    return jsonify(result)
...
```

## Vue Setup